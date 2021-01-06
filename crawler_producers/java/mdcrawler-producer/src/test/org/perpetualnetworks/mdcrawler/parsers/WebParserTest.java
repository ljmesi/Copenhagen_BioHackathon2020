package org.perpetualnetworks.mdcrawler.parsers;

import org.junit.jupiter.api.Test;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertTrue;

class WebParserTest {

    public static final List<String> STRING_LIST = Arrays.asList("DATASET",
            "HANZE netCDF data on land use, population, GDP and wealth in Europe, 1870-2020 (updated)",
            "Dataset posted on 31.10.2017 in 4TU.ResearchData", "Dominik Paprotny");

    private final WebParser webParser = new WebParser();

    @Test
    void typeParing_OK() {
        List<String> testString = Arrays.asList("DATASET:", "test", "posted");
        Optional<String> type = webParser.parseType(testString);
        assertTrue(type.isPresent());
    }

    @Test
    void typeParing_fail() {
        List<String> testString = Arrays.asList("test", "posted");
        Optional<String> type = webParser.parseType(testString);
        assertTrue(type.isEmpty());
    }

    @Test
    void parseTitle() {
        webParser.parseTitle(STRING_LIST);
    }

    @Test
    void parseAuthor() {
        webParser.parseAuthor(STRING_LIST);
    }

    @Test
    void parseDate() {
        Optional<String> date = webParser.parsePostedDate(STRING_LIST);
        if (date.isPresent()) {
            SimpleDateFormat format = new SimpleDateFormat("dd.MM.yyyy");
            try {
                System.out.println("date: " + format.parse(date.get()));
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }
    }
}