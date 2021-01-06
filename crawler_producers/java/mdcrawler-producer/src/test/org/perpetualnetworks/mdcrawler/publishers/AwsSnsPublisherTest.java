package org.perpetualnetworks.mdcrawler.publishers;

import org.junit.jupiter.api.Test;
import org.perpetualnetworks.mdcrawler.config.AwsConfiguration;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

class AwsSnsPublisherTest {

    @Test
    void sendMessage() {
        AwsSnsPublisher publisher = new AwsSnsPublisher(AwsConfiguration.builder()
                .sqsUrl("https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue")
                .credentialsFile("config/aws.json")
                .build());
        SendMessageResponse bob = publisher.sendMessage("hello");
        System.out.println("response: " + bob);
    }
}