package dev.shocolla.spring.model;

import java.util.List;

import org.springframework.data.annotation.Id;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Container(containerName = "course_arrangement", autoCreateContainer = false)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class CourseArrangement {

    @Id
    private String id;

    @PartitionKey
    private String ttid;

    private List<Curriculum> curriculums;

    @Data
    @NoArgsConstructor
    @Accessors(chain = true)
    public static class Curriculum {
        private String homeroom;
        private List<Block> blocks;
    }

    @Data
    @NoArgsConstructor
    @Accessors(chain = true)
    public static class Block {
        private String name;
        private List<Lane> lanes;
    }

    @Data
    @NoArgsConstructor
    @Accessors(chain = true)
    public static class Lane {
        private int index;
        private List<String> courses;
    }
}
