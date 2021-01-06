package org.perpetualnetworks.mdcrawler.services;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.perpetualnetworks.mdcrawler.config.SeleniumConfiguration;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

@Service
public class BrowserAutomatorImpl implements BrowserAutomator {
    public static final String JS_QUERY_SELECTOR_ALL = "return document.querySelectorAll('%s')";
    public static final String FS_DIV_ROLE_ARTICLE = "div[role=article]";
    public static final String FS_HREF_ARTICLE_KEYWORD = "a[href*=keyword]";
    public static final String FS_DIV_ARTICLE_DOI = "div[data-doi]";
    public static final String FS_A_ARTICLE_DOI = "a[href*=doi]";
    public static final String FS_HREF_ARTICLE_CATEGORY = "a[href*=category]";
    public static final String FS_DIV_ARTICLE_ABSTRACT_SPAM = "div";
    public static final String FS_A_ARTICLE_DOWNLOAD = "a[title*=ownload]";
    public static final String FS_SPAN_ARTICLE_FILE_NAME = "span[title]";
    private final SeleniumConfiguration seleniumConfiguration;
    private final WebDriver webDriver;

    @Autowired
    public BrowserAutomatorImpl(SeleniumConfiguration seleniumConfiguration) {
        this.seleniumConfiguration = seleniumConfiguration;
        this.webDriver = createWebDriver();
    }

    @Override
    public void goToPage(String url) {
        webDriver.get(url);
    }

    public List<WebElement> buildPageArticleElements() {
        waitForCssSelector(FS_DIV_ROLE_ARTICLE);
        return fetchAllCurrentFSArticleElements();
    }

    private List<WebElement> fetchAllCurrentFSArticleElements() {
        JavascriptExecutor js = (JavascriptExecutor) webDriver;
        return (List<WebElement>) js.executeScript(buildSelectorQuery(FS_DIV_ROLE_ARTICLE));
    }

    public List<WebElement> fetchAllFSArticleKeywordElements(WebDriver driver) {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        List<WebElement> elements = (List<WebElement>) js.executeScript(buildSelectorQuery(FS_HREF_ARTICLE_KEYWORD));
        elements.addAll((List<WebElement>) js.executeScript(buildSelectorQuery(FS_HREF_ARTICLE_CATEGORY)));
        return elements;
    }

    public List<WebElement> fetchAllFSArticleDoiElements(WebDriver driver) {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        List<WebElement> elements = (List<WebElement>) js.executeScript(buildSelectorQuery(FS_DIV_ARTICLE_DOI));
        elements.addAll((List<WebElement>) js.executeScript(buildSelectorQuery(FS_A_ARTICLE_DOI)));
        return elements;
    }

    public List<WebElement> fetchAllFSArticleAbstracts(WebDriver driver) {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        List<WebElement> elements = (List<WebElement>) js.executeScript(buildSelectorQuery(FS_DIV_ARTICLE_ABSTRACT_SPAM));
        return elements;
    }

    public List<WebElement> fetchAllFSArticleFiles(WebDriver driver) {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        List<WebElement> elements = (List<WebElement>) js.executeScript(buildSelectorQuery(FS_SPAN_ARTICLE_FILE_NAME));
        elements.addAll((List<WebElement>) js.executeScript(buildSelectorQuery(FS_A_ARTICLE_DOWNLOAD)));
        return elements;
    }

    public String buildSelectorQuery(String selector) {
        return String.format(JS_QUERY_SELECTOR_ALL, selector);
    }

    private void waitForCssSelector(String cssSelector) {
        WebDriverWait webDriverWait = new WebDriverWait(webDriver, 5);
        By locator = By.cssSelector(cssSelector);
        ExpectedCondition<WebElement> expectedCon = ExpectedConditions
                .visibilityOfElementLocated(locator);
        webDriverWait.until(expectedCon);
    }

    public void waitByCssSelector(WebDriver webDriver, String cssSelector) {
        WebDriverWait wait = new WebDriverWait(webDriver, 20);
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(cssSelector)));
        webDriver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    public void waitImplicity(WebDriver webDriver, int seconds) {
        webDriver.manage().timeouts().implicitlyWait(seconds, TimeUnit.SECONDS);
    }

    public void agreeToCookies(WebDriver webDriver) {
        webDriver.findElement(By.tagName("button"))
                .sendKeys(Keys.RETURN);
    }


    public WebDriver createWebDriver() {
        ChromeOptions chromeOptions = new ChromeOptions()
                .addArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage", "--silent-output=true");
        System.setProperty(ChromeDriverService.CHROME_DRIVER_SILENT_OUTPUT_PROPERTY, "true");
        return new ChromeDriver(chromeOptions);
    }

    public WebDriver getWebDriver() {
        return this.webDriver;
    }

    public void closeWebDriver() {
        this.webDriver.close();
    }

    public void executeManualScrollDown() {
        IntStream.range(0, 40).forEach(item ->
                this.webDriver.findElement(By.tagName("a"))
                        .sendKeys(Keys.ARROW_DOWN));
    }
}
