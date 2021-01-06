package org.perpetualnetworks.mdcrawler.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;

@Builder
public class Author {
    @JsonProperty
    private String name;
}
