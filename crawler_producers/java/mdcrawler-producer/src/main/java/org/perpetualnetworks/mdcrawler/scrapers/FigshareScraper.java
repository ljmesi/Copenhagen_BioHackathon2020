package org.perpetualnetworks.mdcrawler.scrapers;

import com.google.common.collect.ImmutableSet;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.WebElement;
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
    private static final String FIGSHARE_SEARCH_TERM_URL = "https://figshare.com/search?q=xtc%E2%80%8B%2C%20%E2%80%8Bdcd%2C%E2%80%8B%20%E2%80%8Bntraj%2C%20netcdf%2C%20trr%2C%20lammpstrj%2C%20xyz%2C%20binpos%2C%20hdf5%2C%20dtr%2C%20arc%2C%20tng%2C%20mdcrd%2C%20crd%2C%20dms%2C%20trj%2C%20ent%2C%20ncdf";
    private static final Integer FETCH_LIMIT = 10;
    private final BrowserAutomatorImpl browserAutomator;
    private final FigshareArticleConverter figshareArticleConverter;
    private final AwsSnsPublisher publisher;

    @Autowired
    public FigshareScraper(BrowserAutomatorImpl browserAutomator,
                           FigshareArticleConverter figshareArticleConverter,
                           AwsSnsPublisher publisher) {
        this.browserAutomator = browserAutomator;
        this.figshareArticleConverter = figshareArticleConverter;
        this.publisher = publisher;
    }

    public void runScraper() {
        //Debugging
        log.info("finished waiting, going to page: " + FIGSHARE_SEARCH_TERM_URL);
        log.info("starting get");
        browserAutomator.getWebDriver().get(FIGSHARE_SEARCH_TERM_URL);
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
        if (articles.size() > FETCH_LIMIT) {
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
