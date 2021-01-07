package org.perpetualnetworks.mdcrawler.scrapers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import okhttp3.OkHttpClient;
import okhttp3.Response;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.perpetualnetworks.mdcrawler.config.MendeleyConfiguration;
import org.perpetualnetworks.mdcrawler.converters.MendeleyArticleConverter;
import org.perpetualnetworks.mdcrawler.scrapers.dto.MendeleyResponse;

import java.util.List;

class MendeleyScraperTest {

    private static final MendeleyConfiguration CONFIG = MendeleyConfiguration.builder()
            .host("data.mendeley.com")
            .endPoint("api/research-data/search")
            .searchQuery("molecular trajectories")
            .type("DATASET")
            .build();

    private static final MendeleyArticleConverter MENDELEY_ARTICLE_CONVERTER = new MendeleyArticleConverter();

    @Disabled("works with live data")
    @SneakyThrows
    @Test
    void queryresult() {
        MendeleyScraper scraper = new MendeleyScraper(new OkHttpClient(), CONFIG, MENDELEY_ARTICLE_CONVERTER);
        ObjectMapper mapper = new ObjectMapper();
        Response fetch = scraper.fetch(scraper.buildHttpUrl(1));
        MendeleyResponse responses = mapper.readValue(fetch.body().byteStream(), MendeleyResponse.class);
        System.out.println("responses count: " + responses.getCount() + " size: " + responses.getResults().size());
    }

    @Disabled("works with live data")
    @SneakyThrows
    @Test
    void queryresultAll() {
        MendeleyScraper scraper = new MendeleyScraper(new OkHttpClient(), CONFIG, MENDELEY_ARTICLE_CONVERTER);
        System.out.println("starting fetchall");
        List<MendeleyResponse> responses = scraper.fetchAll();
        System.out.println("ending fetchall, size: " + responses.size());
    }
}