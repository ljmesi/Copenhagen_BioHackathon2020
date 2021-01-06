package org.perpetualnetworks.mdcrawler.parsers;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.util.Strings;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.perpetualnetworks.mdcrawler.models.Author;
import org.perpetualnetworks.mdcrawler.models.FileArticle;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.util.Objects.nonNull;

@Component
@Slf4j
public class WebParser {

    public List<String> parseAllTextElements(WebElement webElement) {
        List<String> textList = new ArrayList<>();
        List<WebElement> elements = webElement.findElements(By.xpath(".//*"));
        if (nonNull(elements)) {
            elements.forEach(element -> {
                String[] split = element.getText().split("\n");
                List<String> strings = Arrays.asList(split);
                strings.forEach(string -> {
                    if (!textList.contains(string)) {
                        textList.add(string);
                    }
                });
            });
        }
        return textList;
    }

    public List<String> parseAllLinks(WebElement webElement) {
        List<String> linkList = new ArrayList<>();
        WebElement element = webElement.findElement(By.xpath(".//a"));
        String href = element.getAttribute("href");
        if (nonNull(href)) {
            linkList.add(href);
        }
        return linkList;
    }

    public Set<String> parseAllKeywords(List<WebElement> webElements) {
        Set<String> keyWords = new HashSet<>();
        webElements.forEach(element ->
                keyWords.add(element.getAttribute("title")));
        webElements.forEach(element ->
                keyWords.add(element.getText()));
        return keyWords.stream().filter(Strings::isNotBlank).collect(Collectors.toSet());
    }

    public Set<String> parseArticleDoi(List<WebElement> webElements) {
        Set<String> dataDoi = new HashSet<>();
        webElements.stream()
                .map(element -> element.getAttribute("data-doi"))
                .filter(Objects::nonNull)
                .forEach(dataDoi::add);
        webElements.stream()
                .map(element -> element.getAttribute("href"))
                .filter(Objects::nonNull)
                .filter(String::isBlank)
                .forEach(dataDoi::add);
        return dataDoi;
    }

    public List<String> parseArticleAbstract(List<WebElement> webElements) {
        List<String> abstracts = new ArrayList<>();
        int citationsIndex = 0;
        int categoriesIndex = 0;
        int counter = 0;
        String[] split = webElements.get(0).getText().split("\n");
        for (String str : split) {
            if (str.startsWith("citations")) {
                citationsIndex = counter;
            }
            if (str.startsWith("CATEGORIES")) {
                categoriesIndex = counter;
            }
            counter++;
        }
        if (citationsIndex != 0 && categoriesIndex != 0) {
            String[] strings = Arrays.copyOfRange(split, citationsIndex + 1, categoriesIndex - 1);
            abstracts.addAll(Arrays.asList(strings));
        }
        return abstracts;
    }

    public Set<FileArticle> parseArticleFiles(List<WebElement> webElements) {
        Set<FileArticle> files = new HashSet<>();
        List<String> fileTitles = new ArrayList<>();
        List<String> downloadLinks = new ArrayList<>();
        webElements.forEach(element -> {
            try {
                String text = element.getText();
                String href = element.getAttribute("href");
                if (text != null) {
                    fileTitles.add(text.replaceAll("\n", ""));
                }
                if (href != null) {
                    downloadLinks.add(href);
                }
            } catch (Exception e) {
                log.warn("exception found while getting web element details");
            }
        });
        if (CollectionUtils.isNotEmpty(fileTitles) && CollectionUtils.isNotEmpty(downloadLinks)) {
            log.info("building file set");
            try {
                for (var i = 0; downloadLinks.size() > i; i++) {
                    files.add(FileArticle.builder()
                            .fileName(fileTitles.get(i))
                            .downloadUrl(downloadLinks.get(i))
                            .build());
                }
            } catch (Exception e) {
                log.error("could not add file", e);
            }
        }
        return files;
    }

    public Optional<String> parsePostedDate(List<String> textElements) {
        final String DATE_REGEX = ".*([0-9]{2}[.][0-9]{2}[.][0-9]{4}).*";
        Pattern pattern = Pattern.compile(DATE_REGEX);
        return textElements.stream()
                .map(string -> string.replace(":", ""))
                .filter(string -> !StringUtils.isAllUpperCase(string))
                .filter(string -> string.split(" ").length > 4)
                .map(string -> {
                    Matcher matcher = pattern.matcher(string);
                    if (matcher.matches()) {
                        return matcher.group(1);
                    }
                    return null;
                })
                .filter(StringUtils::isNotEmpty)
                .findFirst();
    }

    public Optional<Author> parseAuthor(List<String> textElements) {
        return textElements.stream()
                .map(string -> string.replace(":", ""))
                .filter(string -> !StringUtils.isAllUpperCase(string))
                .filter(string -> !StringUtils.containsIgnoreCase("posted", string))
                .filter(string -> string.split(" ").length < 5)
                .findFirst()
                .map(name -> Author.builder().name(name).build());
    }

    public Optional<String> parseTitle(List<String> textElements) {
        if (nonNull(textElements) && textElements.size() > 1) {
            if (textElements.get(0).equals("DATASET")) {
                return Optional.of(textElements.get(1));
            }
            if (textElements.get(0).equals("SOFTWARE")) {
                return Optional.of(textElements.get(1));
            }
        }
        return textElements.stream()
                .map(string -> string.replace(":", ""))
                .filter(string -> !StringUtils.isAllUpperCase(string))
                .filter(string -> !StringUtils.containsIgnoreCase("posted", string))
                .filter(string -> string.split(" ").length > 4)
                .findFirst();
    }

    public Optional<String> parseType(List<String> textElements) {
        return textElements.stream()
                .map(string -> string.replace(":", ""))
                .filter(StringUtils::isAllUpperCase)
                .findFirst();
    }
}
