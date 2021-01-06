package org.perpetualnetworks.mdcrawler.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;

import java.util.Set;

@Builder
public class FileArticle {
    @JsonProperty
    private String fileName;
    @JsonProperty
    private String url;
    @JsonProperty
    private String downloadUrl;
    @JsonProperty
    private String digitalObjectId;
    @JsonProperty
    private String fileDescription;
    @JsonProperty
    private String referingUrl;
    @JsonProperty
    private Set<String> keywords;
}
