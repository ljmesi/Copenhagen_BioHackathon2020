package org.perpetualnetworks.mdcrawler.scrapers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import okhttp3.OkHttpClient;
import okhttp3.Response;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.perpetualnetworks.mdcrawler.config.MendeleyConfiguration;
import org.perpetualnetworks.mdcrawler.converters.MendeleyArticleConverter;
import org.perpetualnetworks.mdcrawler.publishers.AwsSnsPublisher;
import org.perpetualnetworks.mdcrawler.scrapers.dto.MendeleyResponse;

import java.util.List;

class MendeleyScraperTest {

    @Mock
    AwsSnsPublisher publisher;

    private static final MendeleyConfiguration CONFIG = MendeleyConfiguration.builder()
            .host("data.mendeley.com")
            .endPoint("api/research-data/search")
            .searchQuery("molecular trajectories")
            .type("DATASET")
            .build();

    private static final MendeleyArticleConverter MENDELEY_ARTICLE_CONVERTER = new MendeleyArticleConverter();
    public static final ObjectMapper MAPPER = new ObjectMapper();

    @Disabled("works with live data")
    @SneakyThrows
    @Test
    void queryresult() {
        MendeleyScraper scraper = new MendeleyScraper(new OkHttpClient(), CONFIG, MENDELEY_ARTICLE_CONVERTER, publisher);
        Response fetch = scraper.fetch(scraper.buildHttpUrl(1));
        MendeleyResponse responses = MAPPER.readValue(fetch.body().byteStream(), MendeleyResponse.class);
        System.out.println("responses count: " + responses.getCount() + " size: " + responses.getResults().size());
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(responses.getResults()));
    }

    @Disabled("works with live data")
    @SneakyThrows
    @Test
    void queryresultAll() {
        MendeleyScraper scraper = new MendeleyScraper(new OkHttpClient(), CONFIG, MENDELEY_ARTICLE_CONVERTER, publisher);
        System.out.println("starting fetchall");
        List<MendeleyResponse> responses = scraper.fetchAll();
        System.out.println("ending fetchall, size: " + responses.size());
    }
}
