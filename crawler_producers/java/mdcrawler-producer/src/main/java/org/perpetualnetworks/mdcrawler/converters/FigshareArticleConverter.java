package org.perpetualnetworks.mdcrawler.converters;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections.CollectionUtils;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.perpetualnetworks.mdcrawler.models.Article;
import org.perpetualnetworks.mdcrawler.models.Author;
import org.perpetualnetworks.mdcrawler.models.FileArticle;
import org.perpetualnetworks.mdcrawler.parsers.WebParser;
import org.perpetualnetworks.mdcrawler.services.BrowserAutomatorImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.sql.Timestamp;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

import static java.util.Objects.nonNull;

@Component
@Slf4j
public class FigshareArticleConverter {

    private WebParser webParser;

    @Autowired
    public FigshareArticleConverter(WebParser webParser) {
        this.webParser = webParser;
    }


    public Optional<Article> buildArticleFromElement(WebElement webElement) {
        try {
            List<String> textElements = webParser.parseAllTextElements(webElement);
            Article.ArticleBuilder builder = buildArticle(textElements);
            List<String> urls = webParser.parseAllLinks(webElement);
            List<String> sourceUrls = urls.stream().filter(url -> url.startsWith("http")).collect(Collectors.toList());
            sourceUrls.stream().findFirst().ifPresent(builder::sourceUrl);
            Article article = builder.build();
            //log.info("returning article from build: " + article);
            return Optional.of(article);
        } catch (Exception e) {
            log.error("error: " + e.getMessage());
        }
        return Optional.empty();
    }
    public Article.ArticleBuilder buildArticle(List<String> textElements) {
        Article.ArticleBuilder builder = Article.builder();
        Optional<Author> author = webParser.parseAuthor(textElements);
        Optional<String> title = webParser.parseTitle(textElements);
        webParser.parseType(textElements).ifPresent(string -> {
            builder.additionalData(Article.AdditionalData.builder().figshareType(string).build());
        });
        Optional<String> date = webParser.parsePostedDate(textElements);
        author.ifPresent(parsedAuthor -> builder.authors(Collections.singleton(parsedAuthor)));
        title.ifPresent(builder::title);
        if (title.isEmpty()) {
            log.warn("could not parse title from text: " + textElements);
        }
        date.ifPresent(builder::uploadDate);
        return builder;
    }

    public Article updateArticleBySecondaryLink(Article article, BrowserAutomatorImpl browserAutomator, WebParser parser) {
        log.info("starting secondary parse");
        Article.ArticleBuilder builder = article.toBuilder();
        WebDriver driver = browserAutomator.createWebDriver();
        driver.get(article.getSourceUrl());
        browserAutomator.waitImplicity(driver, 5);
        if (article.getAdditionalData() != null) {
            log.info("parsing article type: " + article.getAdditionalData().getFigshareType());
        }
        Set<String> keywords = parser.parseAllKeywords(browserAutomator.fetchAllFSArticleKeywordElements(driver));
        log.info("keyword set not empty: " + CollectionUtils.isNotEmpty(keywords));
        builder.keywords(keywords);
        Set<String> dois = parser.parseArticleDoi(browserAutomator.fetchAllFSArticleDoiElements(driver));
        log.info("secondary dois not empty: " + CollectionUtils.isNotEmpty(dois));
        dois.stream().filter(Objects::nonNull).findFirst().ifPresent(builder::digitalObjectId);
        Timestamp ts = new Timestamp(Instant.now().toEpochMilli());
        builder.parseDate(ts.toLocalDateTime().toString());
        List<String> abstracts = webParser.parseArticleAbstract(browserAutomator.fetchAllFSArticleAbstracts(driver));
        log.info("abstracts not empty: " + CollectionUtils.isNotEmpty(abstracts));
        if (CollectionUtils.isNotEmpty(abstracts)) {
            builder.description(String.join(" ", abstracts));
        }
        Set<FileArticle> fileArticles = webParser.parseArticleFiles(browserAutomator.fetchAllFSArticleFiles(driver));
        builder.files(fileArticles);
        log.info("files not empty: " + CollectionUtils.isNotEmpty(fileArticles) + " size: " + fileArticles.size());
        if (fileArticles.size() == 0 && nonNull(article.getAdditionalData()) && !article.getAdditionalData().getFigshareType().equals("COLLECTION")) {
            log.warn("zero files collected from article: " + article);
        }
        //log.info("returning article from secondary: " + builder.build());
        driver.close();
        return builder.build();
    }
}
