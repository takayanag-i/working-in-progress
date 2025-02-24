package dev.shocolla.spring.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import dev.shocolla.spring.model.Constraint;
import dev.shocolla.spring.service.ConstraintService;

@RestController
@RequestMapping("/api/constraints")
public class ConstraintController {
    @Autowired
    private ConstraintService constraintService;

    @PostMapping
    public ResponseEntity<Constraint> createConstraint(@RequestBody Constraint constraint) {
        Constraint savedConstraint = constraintService.saveConstraint(constraint);
        return ResponseEntity.ok(savedConstraint);
    }
}
