package org.perpetualnetworks.mdcrawler.config;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties("aws")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class AwsConfiguration {
    @JsonProperty
    private String sqsUrl;
    @JsonProperty
    private String credentialsFile;
}
