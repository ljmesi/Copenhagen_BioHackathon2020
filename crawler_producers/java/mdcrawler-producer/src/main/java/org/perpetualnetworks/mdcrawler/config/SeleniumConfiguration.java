package org.perpetualnetworks.mdcrawler.config;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties("selenium")
public class SeleniumConfiguration {
    @JsonProperty("chrome-driver-location")
    private String chromeDriverLocation;
    @JsonProperty
    private String testUrl;

}
