package org.perpetualnetworks.mdcrawler.scrapers.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
@JsonDeserialize(builder = MendeleyResponse.MendeleyResponseBuilder.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class MendeleyResponse {
    @JsonProperty
    private List<Result> results;
    @JsonProperty
    private String query;
    @JsonProperty
    private Integer count;
    @JsonProperty
    private String versionNumber;
    @JsonProperty
    private List<String> promotedResultIds;
    @JsonProperty
    private JsonNode facets;

    @Data
    @Builder
    @JsonDeserialize(builder = Result.ResultBuilder.class)
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Result {
        @JsonProperty
        private String id;
        @JsonProperty("authorsEntities")
        private List<Author> authorEntities;
        @JsonProperty("relatedIdentifierEntities")
        private List<RelatedEntity> relatedEntities;
        @JsonProperty
        private String externalId;
        @JsonProperty
        private String containerTitle;
        @JsonProperty
        private String containerType;
        @JsonProperty
        private String externalContainerType;
        @JsonProperty
        private String source;
        @JsonProperty
        private String lastImported;
        @JsonProperty
        private String lastUpdated;
        @JsonProperty
        private String containerDescription;
        @JsonProperty
        private String doi;
        @JsonProperty
        private String publicationDate;
        @JsonProperty
        private List<String> containerDataTypes;
        @JsonProperty
        private String dateCreated;
        @JsonProperty
        private String dateAvailable;
        @JsonProperty
        private String externalDateModified;
        @JsonProperty
        private String repoType;
        @JsonProperty
        private String funding;
        @JsonProperty
        private String accessRights;
        @JsonProperty
        private String containerURI;
        @JsonProperty
        private List<String> externalSubjectAreas;
        @JsonProperty
        private List<Author> authors;
        @JsonProperty
        private String name;
        @JsonProperty
        private List<String> assetTypes;
        @JsonProperty
        private List<String> snippets;
        @JsonProperty
        private List<String> containerKeywords;
        @JsonProperty
        private String language;
        @JsonProperty
        private List<String> relatedResources;
        @JsonProperty
        private List<String> institutions;
        @JsonProperty
        @JsonIgnore
        private Object institutionsEntities;
        @JsonProperty
        @JsonIgnore
        private List<String> institutionsIds;
        @JsonProperty
        @JsonIgnore
        private String institutionName;
        @JsonProperty
        private String version;
        @JsonProperty
        private String method;
        @JsonProperty
        private Object howToCite;
        @JsonProperty
        @JsonIgnore
        private List<String> journals;
        @JsonProperty
        @JsonIgnore
        private List<String> journalsIssn;
        @JsonProperty
        @JsonIgnore
        private List<String> isSupplementToDoi;
        @JsonProperty
        @JsonIgnore
        private Object journalsEntities;
        @JsonProperty
        @JsonIgnore
        private List<String> subjectAreas;
    }

    @Data
    @Builder
    @JsonDeserialize(builder = Author.AuthorBuilder.class)
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Author {
        @JsonProperty
        private String name;
        @JsonProperty
        private String firstName;
        @JsonProperty
        private String lastName;
        @JsonProperty
        private String nameType;
        @JsonProperty
        private String role;
        @JsonProperty
        private String givenName;
        @JsonProperty
        private String familyName;
        @JsonProperty
        private String orcidId;
        @JsonProperty
        private String source;
        @JsonProperty
        @JsonIgnore
        private Object affiliations;
        @JsonProperty
        @JsonIgnore
        private Object identifiers;
        @JsonProperty
        private String mendeleyProfileId;
        @JsonProperty
        private List<String> scopusAuthorId;
        @JsonProperty
        @JsonIgnore
        private String institutionName;
    }

    @Data
    @Builder
    @JsonDeserialize(builder = RelatedEntity.RelatedEntityBuilder.class)
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class RelatedEntity{
        @JsonProperty
        private String relationType;
        @JsonProperty
        private String id;
        @JsonProperty
        private String idType;
    }

    /*
        "facets" : {
        "range" : {
            "publicationDate" : {
                "min" : "1972-01-01",
                        "max" : "2021-01-01"
            }
        },
        "list" : {
            "repositoryType" : {
                "NON_ARTICLE_BASED_REPOSITORY" : 1984
            },
            "source" : {
                "gbif.gbif" : 1240,
                        "ZENODO" : 240,
                        "MENDELEY_DATA" : 194,
                        "figshare.ars" : 155,
                        "dryad.dryad" : 67,
                        "ethz.marvel" : 11,
                        "APOLLO" : 8,
                        "usc.dl" : 8,
                        "cdl.ucsd" : 4,
                        "gdcc.harvard-dv" : 4,
                        "bl.kcl" : 3,
                        "cisti.osp" : 3,
                        "pu.dataspace" : 1,
                        "tind.caltech" : 1,
                        "umd.lib" : 1
            },
            "type" : {
                "IMAGE" : 9291,
                        "TABULAR_DATA" : 5330,
     */

}
