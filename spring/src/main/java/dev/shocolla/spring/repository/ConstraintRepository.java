package dev.shocolla.spring.repository;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import dev.shocolla.spring.model.Constraint;

import org.springframework.stereotype.Repository;

@Repository
public interface ConstraintRepository extends CosmosRepository<Constraint, String> {
    public Constraint findByTtid(String ttid);
}
