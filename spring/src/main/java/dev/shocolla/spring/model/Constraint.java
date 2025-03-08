package dev.shocolla.spring.model;

import java.util.List;

import org.springframework.data.annotation.Id;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Container(containerName = "constraints", autoCreateContainer = false)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class Constraint {

    /** Cosmos必須ID */
    @Id
    private String id;

    /** 制約 */
    private String constraintType;

    /** パラメータ */
    private List<String> parameters;

    /** 時間割ID */
    @PartitionKey
    private String ttid;
}
