package dev.shocolla.spring.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.azure.cosmos.CosmosClientBuilder;
import com.azure.spring.data.cosmos.config.AbstractCosmosConfiguration;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.spring.data.cosmos.repository.config.EnableCosmosRepositories;

@Configuration
@EnableCosmosRepositories
public class CosmosConfiguration extends AbstractCosmosConfiguration {

    @Value("${azure.cosmos.uri}")
    private String cosmosUri;

    @Value("${azure.cosmos.key}")
    private String cosmosKey;

    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();

        return new CosmosClientBuilder()
                .endpoint(cosmosUri)
                .key(cosmosKey);
    }

    /**
     * データベース名を返却する
     * 
     * @return the database name
     */
    @Override
    public String getDatabaseName() {
        return "cosmicworks";
    }
}
