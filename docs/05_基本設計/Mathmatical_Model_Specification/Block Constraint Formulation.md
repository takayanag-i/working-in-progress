# Block Constraint Formulation

## Introduction
The Block Constraint ensures that within a given block of courses, all lanes have the same number of scheduled courses. This constraint is applied to each homeroom class $h$, each day $d$, and each period $p$.

## Mathematical Formulation
### Notation:
- $H$ - Set of homeroom classes
- $D$ - Set of days
- $P_{h,d}$ - Set of periods for homeroom $h$ on day $d$
- $B_h$ - Set of blocks assigned to homeroom $h$
- $L_b$ - Set of lanes within block $b$
- $C_{l}$ - Set of courses in lane $l$
- $x_{h,d,p,c} \in \{0,1\}$ - Binary variable indicating if course $c$ is scheduled in homeroom $h$, day $d$, period $p$

For each homeroom $h$, each day $d$, and each period $p$, the constraint is formulated as:

$$
\sum_{c \in C_{l_1}} x_{h,d,p,c} = \sum_{c \in C_{l_2}} x_{h,d,p,c}, \quad \forall h \in H, \forall d \in D, \forall p \in P_{h,d}, \forall b \in B_h, \forall l_1, l_2 \in L_b, l_1 \neq l_2.
$$

This ensures that for each block, all lanes have the same sum of assigned courses across periods.

## Implementation in Python
In the Python implementation using PuLP, the constraint is applied as follows:

```python
constraints = [
    lane_sums[0] == lane_sum
    for h in model.data.H
    for d in model.data.D
    for p in model.data.periods[h][d]
    for block in model.data.curriculums[h] if len(block) > 1
    and (
        lane_sums := [
            pulp.lpSum([model.x[h, d, p, c] for c in lane])
            for lane in block
        ]
    )
    for lane_sum in lane_sums[1:]
]
```

## Conclusion
This constraint enforces balanced scheduling across lanes in each block, ensuring fair distribution of course assignments.