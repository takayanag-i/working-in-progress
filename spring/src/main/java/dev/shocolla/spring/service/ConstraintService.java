package dev.shocolla.spring.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import dev.shocolla.spring.model.Constraint;
import dev.shocolla.spring.repository.ConstraintRepository;

@Service
public class ConstraintService {
    @Autowired
    private ConstraintRepository constraintRepository;

    public Constraint saveConstraint(Constraint constraint) {
        return constraintRepository.save(constraint);
    }
}
