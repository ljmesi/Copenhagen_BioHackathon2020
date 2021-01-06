package org.perpetualnetworks.mdcrawler.scrapers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import okhttp3.Call;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.perpetualnetworks.mdcrawler.config.MendeleyConfiguration;
import org.perpetualnetworks.mdcrawler.scrapers.dto.MendeleyResponse;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class MendeleyScraper {

    private final OkHttpClient client;
    private final MendeleyConfiguration mendeleyConfiguration;

    public MendeleyScraper(OkHttpClient client, MendeleyConfiguration mendeleyConfiguration) {
        this.client = client;
        this.mendeleyConfiguration = mendeleyConfiguration;
    }

    @SneakyThrows
    public Response fetch() {
        Request request = new Request.Builder().url(mendeleyConfiguration.getQueryUrl()).build();
        return client.newCall(request).execute();
    }

}
