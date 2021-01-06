package org.perpetualnetworks.mdcrawler.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;

import java.util.Set;

@Data
@Builder(toBuilder = true)
public class Article {
    @JsonProperty
    private String title;
    @JsonProperty
    private String sourceUrl;
    @JsonProperty
    private Set<String> keywords;
    @JsonProperty
    private String digitalObjectId;
    @JsonProperty
    private String description;
    @JsonProperty
    private String parseDate;
    @JsonProperty
    private String uploadDate;
    @JsonProperty
    private Set<FileArticle> files;
    @JsonProperty
    private Set<Author> authors;
    @JsonProperty
    private String referingUrl;  //was parent request url
    @JsonProperty
    private Boolean enriched;
    @JsonProperty
    private Boolean published;
    @JsonProperty
    private AdditionalData additionalData;

    @Data
    @Builder(toBuilder = true)
    public static class AdditionalData {
        @JsonProperty
        private String figshareType;
    }

}
