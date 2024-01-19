/*
 * Copyright 2023-2023 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.cloudfoundry.samples.music.config.ai;

import org.springframework.ai.client.AiClient;
import org.springframework.ai.embedding.EmbeddingClient;
import org.springframework.ai.retriever.VectorStoreRetriever;
import org.springframework.ai.vectorstore.PgVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.InMemoryVectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.jdbc.core.JdbcTemplate;

/**
 *
 * @author Christian Tzolov
 */
@Configuration
@Profile("llm")
public class AiConfiguration {

	@Bean
	public VectorStoreRetriever vectorStoreRetriever(VectorStore vectorStore) {
		return new VectorStoreRetriever(vectorStore);
	}

	@Bean
	public VectorStoreInitializer vectorStoreInitializer(VectorStore vectorStore) {
		return new VectorStoreInitializer(vectorStore);
	}

	@Bean
	public MessageRetriever messageRetriever(VectorStoreRetriever vectorStoreRetriever, AiClient aiClient) {
		return new MessageRetriever(vectorStoreRetriever, aiClient);
	}

}
