package org.perpetualnetworks.mdcrawler.scheduledtasks;

import lombok.extern.slf4j.Slf4j;
import org.perpetualnetworks.mdcrawler.scrapers.FigshareScraper;
import org.perpetualnetworks.mdcrawler.scrapers.MendeleyScraper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class MendeleyTask {
    @Autowired
    MendeleyScraper mendeleyScraper;

    @Scheduled(fixedRate = 3*60*60*1000)
    public void run() {
        log.info("starting scheduled task mendeley scrape");
        mendeleyScraper.runScraper();
        log.info("endinging scheduled task mendeley scrape");
    }

}
