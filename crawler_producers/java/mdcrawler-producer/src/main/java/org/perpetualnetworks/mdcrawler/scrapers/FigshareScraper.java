package org.perpetualnetworks.mdcrawler.scrapers;

import com.google.common.collect.ImmutableSet;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.WebElement;
import org.perpetualnetworks.mdcrawler.config.FigshareConfiguration;
import org.perpetualnetworks.mdcrawler.converters.FigshareArticleConverter;
import org.perpetualnetworks.mdcrawler.models.Article;
import org.perpetualnetworks.mdcrawler.parsers.WebParser;
import org.perpetualnetworks.mdcrawler.publishers.AwsSnsPublisher;
import org.perpetualnetworks.mdcrawler.services.BrowserAutomatorImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

@Component
@Slf4j
public class FigshareScraper {
    private final FigshareConfiguration figshareConfiguration;
    private final BrowserAutomatorImpl browserAutomator;
    private final FigshareArticleConverter figshareArticleConverter;
    private final AwsSnsPublisher publisher;

    @Autowired
    public FigshareScraper(FigshareConfiguration figshareConfiguration,
                           BrowserAutomatorImpl browserAutomator,
                           FigshareArticleConverter figshareArticleConverter,
                           AwsSnsPublisher publisher) {
        this.figshareConfiguration = figshareConfiguration;
        this.browserAutomator = browserAutomator;
        this.figshareArticleConverter = figshareArticleConverter;
        this.publisher = publisher;
    }

    public void runScraper() {
        //Debugging
        log.info("finished waiting, going to page: " + figshareConfiguration.getQueryUrl());
        log.info("starting get");
        browserAutomator.getWebDriver().get(figshareConfiguration.getQueryUrl());
        log.info("waiting for article divs");
        String selector = "div[role=article]";
        browserAutomator.waitByCssSelector(browserAutomator.getWebDriver(), selector);
        log.info("agreeing to cookies");
        browserAutomator.agreeToCookies(browserAutomator.getWebDriver());
        log.info("fetching initial webelements");
        List<WebElement> initialWebElements = browserAutomator.buildPageArticleElements();
        log.info("starting batching for new articles");
        //TODO: parallelize secondary fetching
        Set<Article> articles = fetchNewArticlesByBatch(browserAutomator, ImmutableSet.copyOf(initialWebElements), new HashSet<>());
        log.info("finished batching for articles");
        log.info("closing webdriver");
        browserAutomator.closeWebDriver();
        log.info("starting publish");
        List<SendMessageResponse> sendResponses = articles.stream().map(publisher::sendArticle).collect(Collectors.toList());
        //TODO: assert all messages sent successfully, alert/log if not
        //TODO: add monitoring for messages sent
        log.info("send message responses: " + sendResponses);
    }

    private Set<Article> fetchNewArticlesByBatch(BrowserAutomatorImpl browserAutomator, Set<WebElement> existingList, Set<Article> articles) {
        if (articles.size() > figshareConfiguration.getFetchLimit()) {
            log.info("fetch limit exceeded");
            return articles;
        }
        log.info("starting new batch article fetch");
        int initArticleSize = articles.size();
        boolean isSame = true;
        WebParser webParser = new WebParser();
        browserAutomator.waitImplicity(browserAutomator.getWebDriver(), 5);
        existingList.forEach(element -> {
            Optional<Article> article = figshareArticleConverter.buildArticleFromElement(element);
            article.ifPresent(value -> articles.add(
                    figshareArticleConverter.updateArticleBySecondaryLink(value, browserAutomator, webParser)));
        });
        browserAutomator.waitImplicity(browserAutomator.getWebDriver(), 5);
        Set<WebElement> elementList = new HashSet<>();
        while (isSame) {
            elementList.addAll(browserAutomator.buildPageArticleElements());
            isSame = checkAllElementsAreSame(elementList, existingList);
            log.info("same check: " + isSame + " executing manual scroll");
            browserAutomator.executeManualScrollDown();
        }
        log.info("exiting loop, begining batch fetch");
        if (articles.size() != initArticleSize) {
            fetchNewArticlesByBatch(browserAutomator, existingList, articles);
        }
        return articles;
    }

    private Boolean checkAllElementsAreSame(Set<WebElement> newElementList, Set<WebElement> existingElementList) {
        return newElementList.containsAll(existingElementList) && existingElementList.containsAll(newElementList);
    }

}
