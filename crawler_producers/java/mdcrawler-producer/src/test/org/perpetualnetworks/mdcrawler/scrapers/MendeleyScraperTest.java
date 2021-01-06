package org.perpetualnetworks.mdcrawler.scrapers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import okhttp3.OkHttpClient;
import okhttp3.Response;
import org.junit.jupiter.api.Test;
import org.perpetualnetworks.mdcrawler.config.MendeleyConfiguration;
import org.perpetualnetworks.mdcrawler.scrapers.dto.MendeleyResponse;

import static org.junit.jupiter.api.Assertions.*;

class MendeleyScraperTest {

    @SneakyThrows
    @Test
    void queryresult() {
        MendeleyScraper scraper = new MendeleyScraper(new OkHttpClient(),
                MendeleyConfiguration.builder().queryUrl("https://data.mendeley.com/api/research-data/search?search=molecular%20trajectories&type=DATASET&page=1")
                        .build());
        Response bob = scraper.fetch();
        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(
                mapper.readValue(bob.body().byteStream(), MendeleyResponse.class)));
    }
}