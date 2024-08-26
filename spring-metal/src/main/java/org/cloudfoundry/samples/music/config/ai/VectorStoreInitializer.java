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

import org.cloudfoundry.samples.music.web.AIController;

import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;


import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;

import org.springframework.beans.factory.BeanFactoryUtils;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.ApplicationListener;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.cloudfoundry.samples.music.domain.Album;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.CrudRepository;

import org.springframework.core.annotation.Order;

/**
 *
 * @author Christian Tzolov
 */
@Order(2)
public class VectorStoreInitializer implements ApplicationListener<ApplicationReadyEvent> {

    private static final Logger logger = LoggerFactory.getLogger(VectorStoreInitializer.class);

    private VectorStore vectorStore;

    private CrudRepository<Album, String> repository;

    public VectorStoreInitializer(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @Override
    @SuppressWarnings("unchecked")
    public void onApplicationEvent(ApplicationReadyEvent event) {
        this.repository =  BeanFactoryUtils.beanOfTypeIncludingAncestors(event.getApplicationContext(), CrudRepository.class);
        Iterable<Album> albums = repository.findAll();
        List<Document> documents = new ArrayList<>();


        List<Document> docs = this.vectorStore.similaritySearch("album");
        logger.info("Vector store contains " + docs.size() + " records");

        if (docs.size() == 0) {
            logger.info("Populating vector store");
            for (Album album : albums) {

                String albumDoc = AIController.generateVectorDoc(album);
                documents.add(new Document(album.getId(), albumDoc, new HashMap<>()));

            }
            this.vectorStore.add(documents);
        }
    }
}
