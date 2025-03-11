# Block Constraint

## Overview
The Block Constraint ensures that within a given block of courses, all lanes have the same number of scheduled courses. This constraint is applied to each homeroom class $h$, each day $d$, and each period $p$.

## Mathematical Formulation
Notation:

- $H$  : Set of homeroom classes
- $D$  : Set of days
- $P_{h,d}$  : Set of periods for homeroom $h$ on day $d$
- $B_h$  : Set of blocks assigned to homeroom $h$
- $L_b$  : Set of lanes within block $b$
- $C_{l}$  : Set of courses in lane $l$
- $x_{h,d,p,c} \in \{0,1\}$  : Binary variable indicating if course $c$ is scheduled in homeroom $h$, day $d$, period $p$

The constraint is formulated as:

$$
\sum_{c \in C_{l_1}} x_{h,d,p,c} = \sum_{c \in C_{l_2}} x_{h,d,p,c}\notag
$$

$$
\forall h \in H, \forall d \in D, \forall p \in P_{h,d}, \forall b \in B_h, \forall l_1, l_2 \in L_b, l_1 \neq l_2.\notag
$$

This ensures that for each block, all lanes have the same sum of assigned courses across periods.

