package org.perpetualnetworks.mdcrawler.publishers;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.perpetualnetworks.mdcrawler.config.AwsConfiguration;
import org.perpetualnetworks.mdcrawler.models.Article;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.awscore.AwsRequestOverrideConfiguration;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

import java.io.File;
import java.util.Optional;

@Component
@Slf4j
public class AwsSnsPublisher {
    private final static ObjectMapper MAPPER = new ObjectMapper();
    public static final String AWS_SECRET_ACCESS_KEY = "aws_secret_access_key";
    public static final String AWS_ACCESS_KEY_ID = "aws_access_key_id";
    private final AwsConfiguration awsConfiguration;
    private AwsBasicCredentials awsBasicCredentials;

    @Autowired
    public AwsSnsPublisher(AwsConfiguration awsConfiguration) {
        this.awsConfiguration = awsConfiguration;
        parseAwsCredentials(awsConfiguration).ifPresent(c -> this.awsBasicCredentials = c);
    }

    @SneakyThrows
    private Optional<AwsBasicCredentials> parseAwsCredentials(AwsConfiguration awsConfiguration) {
        File src = new File(awsConfiguration.getCredentialsFile());
        JsonNode fileJson = MAPPER.readValue(src, JsonNode.class);
        AwsBasicCredentials awsBasicCredentials = AwsBasicCredentials.create(fileJson.get(AWS_ACCESS_KEY_ID).asText(),
                fileJson.get(AWS_SECRET_ACCESS_KEY).asText());
        return Optional.of(awsBasicCredentials);
    }

    @SneakyThrows
    public SendMessageResponse sendArticle(Article article) {
        String serialized = MAPPER.writeValueAsString(article);
        return sendMessage(serialized);
    }

    public SendMessageResponse sendMessage(String message) {
        SqsClient client = SqsClient.create();
        AwsBasicCredentials credentials = AwsBasicCredentials.create(awsBasicCredentials.accessKeyId(), awsBasicCredentials.secretAccessKey());
        SendMessageRequest request = SendMessageRequest.builder()
                .overrideConfiguration(AwsRequestOverrideConfiguration.builder()
                        .credentialsProvider(() -> credentials)
                        .build())
                .messageBody(message)
                .queueUrl(awsConfiguration.getSqsUrl())
                .build();
        return client.sendMessage(request);
    }
}