package org.perpetualnetworks.mdcrawler.scrapers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.perpetualnetworks.mdcrawler.config.MendeleyConfiguration;
import org.perpetualnetworks.mdcrawler.converters.MendeleyArticleConverter;
import org.perpetualnetworks.mdcrawler.publishers.AwsSnsPublisher;
import org.perpetualnetworks.mdcrawler.scrapers.dto.MendeleyResponse;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.stream.IntStream;

@Component
@Slf4j
public class MendeleyScraper {

    private final OkHttpClient client;
    private final MendeleyConfiguration mendeleyConfiguration;
    private final MendeleyArticleConverter mendeleyArticleConverter;
    private final AwsSnsPublisher publisher;
    private final ObjectMapper mapper;

    public MendeleyScraper(OkHttpClient client,
                           MendeleyConfiguration mendeleyConfiguration,
                           MendeleyArticleConverter mendeleyArticleConverter,
                           AwsSnsPublisher publisher) {
        this.client = client;
        this.mendeleyConfiguration = mendeleyConfiguration;
        this.mendeleyArticleConverter = mendeleyArticleConverter;
        this.publisher = publisher;
        this.mapper = new ObjectMapper();
    }

    @SneakyThrows
    public Response fetch(HttpUrl httpUrl) {
        Request request = new Request.Builder().url(httpUrl).build();
        return client.newCall(request).execute();
    }

    public HttpUrl buildHttpUrl(Integer pageNumber) {
        return new HttpUrl.Builder()
                .scheme("https")
                .host(mendeleyConfiguration.getHost())
                .addPathSegments(mendeleyConfiguration.getEndPoint())
                .addQueryParameter("search", mendeleyConfiguration.getSearchQuery())
                .addQueryParameter("type", mendeleyConfiguration.getType())
                .addQueryParameter("page", String.valueOf(pageNumber))
                .build();
    }

    @SneakyThrows
    public Optional<MendeleyResponse> convertResponse(Response response) {
        if (response.isSuccessful()) {
            assert response.body() != null;
            return Optional.of(mapper.readValue(response.body().byteStream(),
                    MendeleyResponse.class));
        }
        return Optional.empty();
    }

    public List<MendeleyResponse> fetchAll() {
        List<MendeleyResponse> responses = new ArrayList<>();
        convertResponse(fetch(buildHttpUrl(1)))
                .ifPresent(response -> responses.addAll(fetchRemaining(response)));
        return responses;
    }

    private Set<MendeleyResponse> fetchRemaining(MendeleyResponse response) {
        Set<MendeleyResponse> responses = new HashSet<>();
        Integer count = response.getCount();
        int size = response.getResults() != null ? response.getResults().size() : 10;
        log.info("count: " + count + " size: " + size);
        responses.add(response);
        double pages = Math.ceil((double) count / size);
        System.out.println("pages found: " + pages);
        IntStream.range(2, (int) pages)
                .forEach(page -> {
                    log.info("fetching page: " + page);
                    convertResponse(fetch(buildHttpUrl(page)))
                            .ifPresent(responses::add);
                    log.info("current size: " + responses.size());
                });
        return responses;
    }
    public void runScraper() {
        fetchAll().stream().map(MendeleyResponse::getResults)
                .flatMap(List::stream)
                .map(mendeleyArticleConverter::convert)
                .forEach(publisher::sendArticle);
    }

}
