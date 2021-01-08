package org.perpetualnetworks.mdcrawler.converters;

import lombok.extern.slf4j.Slf4j;
import org.codehaus.plexus.util.StringUtils;
import org.perpetualnetworks.mdcrawler.models.Article;
import org.perpetualnetworks.mdcrawler.models.Author;
import org.perpetualnetworks.mdcrawler.scrapers.dto.MendeleyResponse;
import org.springframework.stereotype.Component;

import java.sql.Date;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

@Component
@Slf4j
public class MendeleyArticleConverter {

    public Article convert(MendeleyResponse.Result result) {
        return Article.builder()
                .title(result.getContainerTitle())
                .digitalObjectId(result.getDoi() == null ? result.getDoi() : result.getExternalId())
                .description(result.getContainerDescription())
                .sourceUrl(result.getContainerURI())
                .uploadDate(result.getDateCreated())
                .parseDate(Date.from(Instant.now()).toString())
                .keywords(parseKeywords(result))
                .enriched(false)
                .additionalData(parseAddtionalData(result))
                .authors(parseAuthors(result))
                .build();
    }

    private HashSet<String> parseKeywords(MendeleyResponse.Result result) {
        HashSet<String> keywords = new HashSet<>(result.getContainerKeywords());
        keywords.addAll(result.getSubjectAreas());
        keywords.addAll(result.getExternalSubjectAreas());
        return keywords;
    }

    private Article.AdditionalData parseAddtionalData(MendeleyResponse.Result result) {
        List<String> details = new ArrayList<>();
        if (result.getMethod() != null) {
            details.add(result.getMethod());
        }
        if (result.getSnippets() != null) {
            details.addAll(result.getSnippets());
        }
        return Article.AdditionalData.builder().labDetails(details).build();
    }
    private Set<Author> parseAuthors(MendeleyResponse.Result result) {
        return result.getAuthors().stream()
                .map(MendeleyResponse.Author::getName)
                .filter(StringUtils::isNotBlank)
                .map(name -> Author.builder().name(name).build())
                .collect(Collectors.toSet());
    }


}
