package dev.shocolla.spring.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.azure.cosmos.CosmosClientBuilder;
import com.azure.spring.data.cosmos.config.AbstractCosmosConfiguration;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.spring.data.cosmos.repository.config.EnableCosmosRepositories;

/**
 * Configuration class for setting up Azure Cosmos DB.
 */
@Configuration
@EnableCosmosRepositories
public class CosmosConfiguration extends AbstractCosmosConfiguration {

    /** The URI of the Azure Cosmos DB. */
    @Value("${azure.cosmos.uri}")
    private String cosmosUri;

    /** The key for accessing the Azure Cosmos DB. */
    @Value("${azure.cosmos.key}")
    private String cosmosKey;

    /** The name of the Azure Cosmos DB database. */
    @Value("${azure.cosmos.database}")
    private String cosmosDatabase;

    /**
     * Creates and returns a CosmosClientBuilder instance.
     * 
     * @return a CosmosClientBuilder instance
     */
    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();

        return new CosmosClientBuilder()
                .endpoint(cosmosUri)
                .key(cosmosKey);
    }

    /**
     * Returns the name of the database.
     * 
     * @return the database name
     */
    @Override
    public String getDatabaseName() {
        return cosmosDatabase;
    }
}
