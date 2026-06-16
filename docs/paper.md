# Programmable Environment Calculus as Theory of Dynamic Software Evolution

# 1. Introduction

This section introduces the background and motivation for our research.

## Software Evolution

Today, computers are used for a variety of purposes and the software in most computers is becoming larger and more complex. Some kinds of software are revised progressively and used continuously without rewriting them overall. We call this process of software growth *software evolution*. Software evolution is one of the important features in advanced computer systems and many people acknowledge the importance of its theoretical study. Software evolution is divided into two categories: static and dynamic evolution. Static evolution involves changes in a software system at the stage before compilation; a typical example is software revision. On the other hand, dynamic evolution means that the changes in the software system are in the execution time. The dynamic library mechanism in operating systems and dynamic class loading in Java are classified as dynamic evolution. In this paper, we propose a calculus with programmable environments, called programmable environment calculus, as a theory of dynamic evolution.

## First-class Environments

An environment is a mapping of variable identifiers to values. In a number of implementations [[9](#ref-9), [7](#ref-7)] of programming language Scheme, we can use runtime environments as first-class citizens, which are entities that can be passed as parameters and returned as resultant values. The operations for first-class environments are classified roughly into the following two categories:

1. **Environment reification**: making a meta-level environment into an object-level entity. The basic primitive of reification in the Scheme implementations is `the-environment`, which returns the current environment.

2. **Environment reflection**: restoring object-level data representing an environment into a meta-level object. The basic primitive of reflection is `(eval expression environment)`, which evaluates the expression in the environment.

The mechanism of first-class environments is applied to module systems and code sharing in functional languages [[8](#ref-8), [5](#ref-5), [16](#ref-16)].

## Explicit Substitutions and Environment Calculus

The idea of explicit substitutions was proposed by Curien et al. [[1](#ref-1), [2](#ref-2)], which is an interesting approach to make substitutions work at object-level in the $\lambda$-calculus, and meta-level environments in the $\lambda$-calculus is formalized as such explicitly-formalized substitutions; the calculus of explicit substitutions is called the $\lambda\sigma$-calculus.

We have studied the environment calculus, which is a $\lambda$-calculus extended by adding first-class environments; we proposed an untyped calculus $\lambda_{\mathrm{env}}$ [[14](#ref-14)], a simply-typed calculus $\lambda^{\to}_{\mathrm{env}}$ [[12](#ref-12)], and an ML-polymorphic calculus $\mathrm{ML}_{\mathrm{env}}$ [[11](#ref-11), [13](#ref-13)]. The key difference of the $\lambda\sigma$-calculus and the environment calculus is that the substitutions in the $\lambda\sigma$-calculus are not defined as terms but another kind of syntactic entities. On the other hand, substitutions in the environment calculus are defined as terms, which belong to the same syntactic category as variables, $\lambda$-abstractions, and function applications. In the $\lambda$-calculus and the $\lambda\sigma$-calculus, the terms are the first-class citizens. Therefore, if we introduce first-class environments into $\lambda\sigma$-calculus, we should allow the substitutions to be permissible in the environment calculus.

## Programmable Environments

From the semantic viewpoint, the first-class environments are functions which maps variables to their bound values. However, we cannot used them as first-class functions in the calculus: the first-class environments are not permissible to take arguments. For example, consider a term $(M/x) . id$ means an environment in which a value of $M$ is bound to a variable $x$. Though we can refer the binding as $x \circ (M/x) . id$[^1], a function application such as $((M/x) . id)N$ is not allowed for any term $N$. In this paper, we try to relax such barrier between functions and environments. This improvement provides us fine and direct control on name spaces. We will see that the programmable environment calculus forms a theory of dynamic software evolution.

[^1]: The term means evaluation of variable $x$ under the first-class environment $(M/x) . id$.


# 2 Programmable Environment Calculus $\lambda_{penv}$

We assume a set $Var$ of variables and use $x, y, z$ for representing variables.

## Definition. Terms of $\lambda_{penv}$

The terms of the calculus $\lambda_{penv}$ are defined inductively as follows:

$$
\begin{aligned}
M ::= {}& x && \text{variables} \\
  \mid{}& \lambda x . M && \text{lambda abstraction} \\
  \mid{}& (M\ N) && \text{function application} \\
  \mid{}& id && \text{environment identity} \\
  \mid{}& (M/x) . N && \text{environment extension} \\
  \mid{}& (M \circ N) && \text{environment composition} \\
  \mid{}& \text{``}x\text{''} && \text{name constants.}
\end{aligned}
$$

The symbol $\equiv$ denotes the syntactic equivalence between the terms. We sometimes use the extended syntax by adding boolean constants, conditional expressions, and comparison between name constants:

$$
M ::= true \mid false \mid \text{if } L \text{ then } M \text{ else } N \mid M = N.
$$

The calculus with such extended syntax is called the extended calculus, and the calculus with the non-extended one is called the pure calculus.

We now give an intuitive explanation of the terms. The variables, the $\lambda$-abstractions, and the function applications have similar meaning to those of the $\lambda$-calculus. The identity environment $id$ means the current environment. This provides environment reification and corresponds to `(the-environment)` in Scheme. The environment extension $(M/x).N$ is a constructor of evaluation values. The environment value is obtained by adding a binding of $M$ to $x$ to the environment $N$. The environment composition $(M \circ N)$ is evaluated to a value of $M$ under the environment $N$. If both $M$ and $N$ have environment values and if we regard environments as substitutions, then $(M \circ N)$ corresponds to the composition of substitutions. This provides environment reflection and corresponds to `(eval (quote M) N)` in Scheme. These six kinds of terms mentioned above give us the syntax of the environment calculus [[11](#ref-11), [12](#ref-12), [14](#ref-14), [13](#ref-13)]. The name constant $\text{``}x\text{''}$ is newly added to the programmable environment calculus. The name constant $\text{``}x\text{''}$ is the variable name of the variable $x$.

The semantics of $\lambda_{penv}$ is given as a translation of $\lambda_{penv}$ into the $\lambda$-calculus, which is based on the environment model of the $\lambda$-calculus. The translation semantics was originally proposed for studying strong normalization of the simply typed environment calculus [[12](#ref-12)].

We assume a one-to-one correspondence $[\![-]\!]$ which maps variables to numerals coded as $\lambda$-terms. For example, we have Church numerals, where $0$ is coded as $\lambda x.\lambda f.x$ and $n$ is coded as $\lambda x.\lambda f.(f(\cdots(fx)))$, where $f$ occurs $n$ times in the body.

We first introduce some terms which provide association lists for representing environments.

## Definition. Lookup and Update

The $\lambda$-terms $Lookup$ and $Update$ are defined respectively as

$$
\begin{aligned}
Update &\equiv \lambda r x q i . (If\ (Equal\ i\ x)\ q\ (r\ i)), \\
Lookup &\equiv \lambda r x . (r\ x),
\end{aligned}
$$

where $Equal$ is a $\lambda$-term which represents the equality predicate on Church numerals and $If$ is a $\lambda$-term which represents conditional, assuming that boolean values are represented as

$$
True = \lambda x y . x
\qquad\text{and}\qquad
False = \lambda x y . y.
$$

The semantic function $[\![ - ]\!](-)$ is a mapping of $\lambda_{penv}$-terms and $\lambda$-terms to $\lambda$-terms defined inductively as follows:

$$
\begin{aligned}
[\![x]\!]\rho &= (Lookup\ \rho\ [\![x]\!]), \\
[\![\lambda x.M]\!]\rho &= \lambda v.[\![M]\!](Update\ \rho\ [\![x]\!]\ v), \\
[\![(M\ N)]\!]\rho &= ([\![M]\!]\rho)([\![N]\!]\rho), \\
[\![id]\!]\rho &= \rho, \\
[\![(M/x).N]\!]\rho &= (Update\ [\![N]\!]\rho\ [\![x]\!]\ [\![M]\!]\rho), \\
[\![(M \circ N)]\!]\rho &= [\![M]\!]([\![N]\!]\rho), \\
[\![\text{``}x\text{''}]\!]\rho &= [\![x]\!],
\end{aligned}
$$

where $\rho$ is a $\lambda$-term and $v$ is a variable which occurs neither in $\lambda x.M$ nor in $\rho$. Moreover, the semantic function is defined to the extended calculus as

$$
\begin{aligned}
[\![true]\!]\rho &= True, \\
[\![false]\!]\rho &= False, \\
[\![\text{if } L \text{ then } M \text{ else } N]\!]\rho
  &= (If\ [\![L]\!]\rho\ [\![M]\!]\rho\ [\![N]\!]\rho), \\
[\![M = N]\!]\rho &= (Equal\ [\![M]\!]\rho\ [\![N]\!]\rho).
\end{aligned}
$$

The first argument is a $\lambda_{penv}$-term to be given the meaning, and the second argument is a $\lambda$-term which represents the current environment.

## Example. Environment Reification

A term $(\lambda x.\lambda y.id)$ is an example including environment reification. The term means a function which returns an environment binding two arguments to the variables $x$ and $y$ respectively.

$$
\begin{aligned}
[\![\lambda x.\lambda y.id]\!]\rho
&= \lambda v.([\![\lambda y.id]\!](Update\ \rho\ [\![x]\!]\ v)) \\
&= \lambda v.\lambda w.[\![id]\!](Update\ (Update\ \rho\ [\![x]\!]\ v)\ [\![y]\!]\ w) \\
&= \lambda v.\lambda w.(Update\ (Update\ \rho\ [\![x]\!]\ v)\ [\![y]\!]\ w).
\end{aligned}
$$

Actually, if terms $M$ and $N$ are applied to this term, then the application $(\lambda x.\lambda y.id)MN$ has the meaning

$$
(Update\ (Update\ \rho\ [\![x]\!]\ [\![M]\!]\rho)\ [\![y]\!]\ [\![N]\!]\rho),
$$

which is an environment including an $x$-binding and a $y$-binding.

## Example. Environment Reflection

Environment reflection represents the environment in which values of $M$ and $N$ are bound to variables $x$ and $y$, respectively. A term $(M/x).(N/y).id$ has the same meaning under the environment $\rho$. A term $(xy) \circ ((\lambda x.\lambda y.id)MN)$ is an example of environment reflection. The subterm

$$
(\lambda x.\lambda y.id)MN
$$

returns an object-level environment. It is reflected to the meta-level environment, and the subterm $(xy)$ is evaluated under the environment:

$$
\begin{aligned}
[\![(xy) \circ ((\lambda x.\lambda y.id)MN)]\!]\rho
&= [\![(xy)]\!]\rho' \\
&\equiv (Lookup\ [\![x]\!]\ \rho') (Lookup\ [\![y]\!]\ \rho') \\
&=_{\beta} ([\![M]\!]\rho\ [\![N]\!]\rho),
\end{aligned}
$$

where

$$
\rho' = (Update\ (Update\ \rho\ [\![x]\!]\ [\![M]\!]\rho)\ [\![y]\!]\ [\![N]\!]\rho).
$$

## Example. Programmable Environments

The key feature of the calculus $\lambda_{penv}$ is the uniform treatment of environments and functions. A term

$$
(\lambda i.\text{ if } i = \text{``}x\text{'' then } M \text{ else } N)
$$

represents a function from name constants to values, which can be treated as an object-level environment. A term

$$
x \circ (\lambda i.\text{ if } i = \text{``}x\text{'' then } M \text{ else } N)
$$

means an evaluation of the variable $x$ under the object-level environment:

$$
\begin{aligned}
&[\![x \circ (\lambda i.\text{ if } i = \text{``}x\text{'' then } M \text{ else } N)]\!]\rho \\
&= [\![x]\!]([\![\lambda i.\text{ if } i = \text{``}x\text{'' then } M \text{ else } N]\!]\rho) \\
&\equiv (Lookup\ (\lambda v. If\ (Equal\ [\![i]\!]\rho'\ [\![\text{``}x\text{''}]\!]\rho')\ [\![M]\!]\rho'\ [\![N]\!]\rho')\ [\![x]\!]) \\
&=_{\beta} (\lambda v.\cdots)\ [\![x]\!] \qquad\text{because of the definition of } Lookup \\
&\equiv (If\ (Equal\ (Lookup\ (Update\ \rho\ [\![i]\!]\ [\![x]\!])\ [\![i]\!])\ [\![x]\!])\ [\![M]\!]\rho''\ [\![N]\!]\rho'') \\
&=_{\beta} (If\ (Equal\ [\![x]\!]\ [\![x]\!])\ [\![M]\!]\rho''\ [\![N]\!]\rho'') \\
&=_{\beta} [\![M]\!]\rho'',
\end{aligned}
$$

where $\rho'$ and $\rho''$ are

$$
\rho' = (Update\ \rho\ [\![i]\!]\ v)
\qquad\text{and}\qquad
\rho'' = (Update\ \rho\ [\![i]\!]\ [\![x]\!]),
$$

respectively. Note that it is essential that $(Lookup\ M\ N)$ is equivalent to the application $(M\ N)$.


# 3 Reduction of $\lambda_{\mathrm{penv}}$

In this section, we introduce the reduction of the programmable environment calculus.

## Definition. Reduction $\to$, $\alpha$-subreduction, $\beta$-subreduction

The reduction of $\lambda_{\mathrm{penv}}$ is a binary relation between terms defined inductively by the following reduction rules.

### The $\alpha$-rules

$$
\begin{array}{rcll}
\mathrm{Assoc} & (L \circ M) \circ N & \to & L \circ (M \circ N) \\
\mathrm{IdL} & \mathrm{id} \circ M & \to & M \\
\mathrm{IdR} & M \circ \mathrm{id} & \to & M \\
\mathrm{DExtn} & ((M/x) . N) \circ L & \to & ((M \circ L)/x) . (N \circ L) \\
\mathrm{VarRef} & x \circ ((M/x) . N) & \to & M \\
\mathrm{VarSkip} & y \circ ((M/x) . N) & \to & y \circ N \quad (x \not\equiv y) \\
\mathrm{DApp} & (M\ N) \circ L & \to & (M \circ L)(N \circ L) \\
\mathrm{AppConst} & M\ ``x'' & \to & x \circ M \\
\mathrm{ConstComp} & ``x'' \circ L & \to & ``x'' \\
\mathrm{VarClos} & x \circ ((\lambda y.M) \circ L) & \to & M \circ ((``x''/y) . L) \\
\mathrm{VarLam} & x \circ (\lambda y.M) & \to & M \circ ((``x''/y) . \mathrm{id})
\end{array}
$$

### The $\beta$-rules

$$
\begin{array}{rcll}
\mathrm{BetaClos} & ((\lambda x.M) \circ L)N & \to & M \circ ((N/x) . L) \\
\mathrm{BetaLam} & (\lambda x.M)N & \to & M \circ ((N/x) . \mathrm{id}) \\
\mathrm{Equal} & (``x'' = ``x'') & \to & \mathrm{true} \\
\mathrm{Inequal} & (``x'' = ``y'') & \to & \mathrm{false} \\
\mathrm{DEqual} & (M = N) \circ L & \to & (M \circ L) = (N \circ L) \\
\mathrm{CondTrue} & \mathrm{if}\ \mathrm{true}\ \mathrm{then}\ M\ \mathrm{else}\ N & \to & M \\
\mathrm{CondFalse} & \mathrm{if}\ \mathrm{false}\ \mathrm{then}\ M\ \mathrm{else}\ N & \to & N \\
\mathrm{DCond} & (\mathrm{if}\ M\ \mathrm{then}\ N_1\ \mathrm{else}\ N_2) \circ L & \to &
\mathrm{if}\ (M \circ L)\ \mathrm{then}\ (N_1 \circ L)\ \mathrm{else}\ (N_2 \circ L)
\end{array}
$$

The subreduction defined by the $\alpha$-rules is called $\alpha$-subreduction and written $\xrightarrow{\alpha}$. We write $M \xrightarrow{\beta} N$ if $M \to N$ but $M \xrightarrow{\alpha} N$ does not hold. Such subreduction is called the $\beta$-subreduction.

The reduction rules given above are obtained from the reduction rules of the environment calculus. These reduction rules originated in the weak reduction with names of the $\lambda\sigma$-calculus.

## Examples

### Environment Reification

The term exemplifying the environment reification is reduced as follows:

$$
\begin{aligned}
(\lambda x.\lambda y.\mathrm{id})MN
&\to_{\mathrm{BetaLam}} ((\lambda y.\mathrm{id}) \circ (M/x).\mathrm{id})N \\
&\to_{\mathrm{BetaClos}} \mathrm{id} \circ ((N/y).(M/x).\mathrm{id}) \\
&\to_{\mathrm{IdL}} (N/y).(M/x).\mathrm{id}.
\end{aligned}
$$

### Environment Reflection

The following term is the example of the environment reflection mentioned in the previous section:

$$
\begin{aligned}
(xy) \circ ((\lambda x.\lambda y.\mathrm{id})MN)
&\to \cdots \\
&\to (xy) \circ ((N/y).(M/x).\mathrm{id}) \\
&\to_{\mathrm{DApp}} (x \circ ((N/y).(M/x).\mathrm{id}))
       (y \circ ((N/y).(M/x).\mathrm{id})) \\
&\to_{\mathrm{VarSkip}} (x \circ ((M/x).\mathrm{id}))
       (y \circ ((N/y).(M/x).\mathrm{id})) \\
&\to_{\mathrm{VarRef}} M(y \circ ((N/y).(M/x).\mathrm{id})) \\
&\to_{\mathrm{VarRef}} (M\ N).
\end{aligned}
$$

### Programmable Environments

As we already mentioned, a function on names

$$
\lambda i.\ \mathrm{if}\ i = ``x''\ \mathrm{then}\ M\ \mathrm{else}\ N
$$

is used as an object-level environment in the following example:

$$
\begin{aligned}
x \circ (\lambda i.\mathrm{if}\ i = ``x''\ \mathrm{then}\ M\ \mathrm{else}\ N)
&\to_{\mathrm{VarLam}} (\mathrm{if}\ i = ``x''\ \mathrm{then}\ M\ \mathrm{else}\ N)
   \circ ((``x''/i).\mathrm{id}) \\
&\to_{\mathrm{DCond}} \mathrm{if}\ ((i = ``x'') \circ L)\ \mathrm{then}\ (M \circ L)\ \mathrm{else}\ (N \circ L) \\
&\to_{\mathrm{DEqual}} \mathrm{if}\ (i \circ L) = (``x'' \circ L)\ \mathrm{then}\ (M \circ L)\ \mathrm{else}\ (N \circ L) \\
&\to_{\mathrm{ConstComp}} \mathrm{if}\ (i \circ ((``x''/i).\mathrm{id})) = ``x''\ \mathrm{then}\ (M \circ L)\ \mathrm{else}\ (N \circ L) \\
&\to_{\mathrm{VarRef}} \mathrm{if}\ ``x'' = ``x''\ \mathrm{then}\ (M \circ L)\ \mathrm{else}\ (N \circ L) \\
&\to_{\mathrm{Equal}} \mathrm{if}\ \mathrm{true}\ \mathrm{then}\ (M \circ L)\ \mathrm{else}\ (N \circ L) \\
&\to_{\mathrm{CondTrue}} M \circ ((``x''/i).\mathrm{id}),
\end{aligned}
$$

where $L$ is $((``x''/i).\mathrm{id})$.

Symmetrically, a first-class environment $((M/x).N)$ is used as a function in the following example:

$$
((M/x).N)``x'' \to_{\mathrm{AppConst}} x \circ ((M/x).N) \to_{\mathrm{VarRef}} M.
$$

## More Complicated Example: Dynamic Library Dispatcher

Java provides dynamic class loading. Its key features are that the classes to be loaded are determined by the identifier names and, moreover, the class loader itself is described in Java. The dynamic class loading mechanism enables each applet to have separate name spaces, which contributes to Java's security. It is proposed that the mechanism of dynamic class loading can be formalized by using first-class environments. Also in our programmable environment calculus $\lambda_{\mathrm{penv}}$, we can represent such dynamic dispatching mechanism in the calculus itself.

We now extend the definition of variables. In Section 2, it is assumed that variables are given. In this section, we assume that a set of identifiers is assumed and the variables are defined as sequences of the identifiers:

$$
x ::= a_1.a_2.\cdots.a_n,
$$

where $n \geq 1$ and $a_1,\ldots,a_n$ are identifiers. Moreover, we introduce the new syntax and the new reduction rules as follows:

$$
M ::= \cdots \mid \mathrm{hd}(M) \mid \mathrm{tl}(M),
$$

$$
\mathrm{hd}(``a_1.a_2.\cdots.a_n'') \to ``a_1'',
$$

$$
\mathrm{tl}(``a'') \to ``a'', \qquad
\mathrm{tl}(``a_1.a_2.\cdots.a_n'') \to ``a_2.\cdots.a_n'' \quad (n \geq 2).
$$

We consider two simple libraries $\mathrm{SysLib}$ and $\mathrm{UsrLib}$, where $x$ is bound to $M_s$ and $M_u$, respectively:

$$
\mathrm{SysLib} = (M_s/x).\mathrm{id}, \qquad
\mathrm{UsrLib} = (M_u/x).\mathrm{id}.
$$

$\mathrm{Dispatcher}$ switches the libraries, depending on the head identifier of each variable. If a variable is prefixed with $\mathrm{system}$, then the library $\mathrm{SysLib}$ is linked; otherwise, the library $\mathrm{UsrLib}$ is linked. The object-level environment $\mathrm{Lib}$ defined below represents a dynamic loader equipped with such a library dispatcher:

$$
\begin{aligned}
\mathrm{Dispatcher} &= \lambda sys.\lambda usr.\lambda i.\
\mathrm{if}\ (\mathrm{hd}(i) = ``system'')\ 
\mathrm{then}\ (sys(\mathrm{tl}(i)))\ 
\mathrm{else}\ (usr(\mathrm{tl}(i))), \\
\mathrm{Lib} &= \mathrm{Dispatcher}\ \mathrm{SysLib}\ \mathrm{UsrLib} \\
&= (\lambda i.\mathrm{if}\ \cdots) \circ ((\mathrm{UsrLib}/usr).(\mathrm{SysLib}/sys).\mathrm{id}).
\end{aligned}
$$

The following two examples show library switching through the loader:

$$
\begin{aligned}
system.x \circ \mathrm{Lib}
&\to \mathrm{Lib}\ ``system.x'' \\
&\to (\mathrm{if}\ \cdots) \circ ((``system.x''/i).\cdots) \\
&\to \mathrm{if}\ (\mathrm{hd}(``system.x'') = ``system'')\ 
\mathrm{then}\ (\mathrm{SysLib}(\mathrm{tl}(``system.x'')))\ 
\mathrm{else}\ (\mathrm{UsrLib}(\mathrm{tl}(``system.x''))) \\
&\to \mathrm{SysLib}(\mathrm{tl}(``system.x'')) \\
&\to \mathrm{SysLib}\ ``x'' \\
&\to x \circ ((M_s/x).\mathrm{id}) \\
&\to M_s,
\end{aligned}
$$

and

$$
\begin{aligned}
x \circ \mathrm{Lib}
&\to \mathrm{Lib}\ ``x'' \\
&\to (\mathrm{if}\ \cdots) \circ ((``x''/i).\cdots) \\
&\to \mathrm{if}\ (\mathrm{hd}(``x'') = ``system'')\ \cdots \\
&\to \mathrm{if}\ (``x'' = ``system'')\ \mathrm{then}\ \cdots\ \mathrm{else}\ (\mathrm{UsrLib}(\mathrm{tl}(``x''))) \\
&\to \mathrm{UsrLib}(\mathrm{tl}(``x'')) \\
&\to \mathrm{UsrLib}\ ``x'' \\
&\to x \circ ((M_u/x).\mathrm{id}) \\
&\to M_u.
\end{aligned}
$$

The reduction enjoys soundness with respect to the semantics introduced in the previous section.

## Theorem. Soundness of Reduction

The reduction $\to$ is sound with respect to the translation semantics: let $M$ and $N$ be $\lambda_{\mathrm{penv}}$-terms. If $M \to N$, then $\llbracket M \rrbracket p = \llbracket N \rrbracket p$ for any $\lambda$-term $p$.


# Concluding Remarks

In this paper, we proposed a calculus with programmable environments, in which we can treat environments and functions without barriers and know that the calculus is regarded as a theory of dynamic software evolution, showing some examples. We would like to finish this paper with comments on related works and future direction of this research.

Recently, Sato et al. [[17](#ref-17)] proposed another environment calculus, called $\lambda e$-calculus. It is based on the simple type system in the explicit typing style. Their calculus also provides first-class environments; programmable environments are not supported in their calculus.

The $\lambda \nu$-calculus is an extension of $\lambda$-calculus with names, proposed by M. Odersky [[15](#ref-15)]. In the calculus, we can use names in a local context of a term, by using a binding construct $\nu n.M$ for names, keeping referential transparency. We may say that it is a rational improvement of a symbol generation construct `gensym` in Lisp. Name constants are available also in $\lambda_{penv}$. However, the calculus $\lambda_{penv}$ provides only global names which cannot be treated as local names, since the calculus lacks a name-localization mechanism like $\nu n$. It is a future work that the name-binding mechanism is compatible to the programmable environment mechanism in $\lambda_{penv}$.

# References

<a id="ref-1"></a>[1] M. Abadi, L. Cardelli, P.-L. Curien, and J.-J. Levy. *Explicit substitutions*. Journal of Functional Programming, 1(4):375-416, October 1991. DOI: [10.1017/S0956796800000186](https://doi.org/10.1017/S0956796800000186)

<a id="ref-2"></a>[2] P.-L. Curien. *An abstract framework for environment machines*. Theoretical Computer Science, 82:389-402, 1991. DOI: [10.1016/0304-3975(91)90230-Y](https://doi.org/10.1016/0304-3975(91)90230-Y)

<a id="ref-3"></a>[3] P.-L. Curien, T. Hardin, and J.-J. Levy. *Confluence properties of weak and strong calculi of explicit substitutions*. Journal of the ACM, 43(2):362-397, March 1996. DOI: [10.1145/226643.226675](https://doi.org/10.1145/226643.226675)

<a id="ref-4"></a>[4] D. Dean. *Formal Aspects of Mobile Code Security*. PhD thesis, Princeton University, January 1999. DOI: [10.5555/929537](https://doi.org/10.5555/929537)

<a id="ref-5"></a>[5] D. Gelernter, S. Jagannathan, and T. London. *Environments as first-class objects*. In *Conference Record of the Fourteenth Annual ACM Symposium on Principles of Programming Languages*, pages 98-110, 1987. DOI: [10.1145/41625.41634](https://doi.org/10.1145/41625.41634)

<a id="ref-6"></a>[6] L. Gong. *Inside Java 2 Platform Security: Architecture, API Design, and Implementation*. Addison-Wesley, 1999. DOI: [10.5555/310688](https://doi.org/10.5555/310688)

<a id="ref-7"></a>[7] C. Hanson. *MIT Scheme Reference Manual*. MIT, 1.62 edition, 1996. DOI未確認。

<a id="ref-8"></a>[8] B. Lampson and R. Burstall. *Pebble, a kernel language for modules and abstract data types*. Information and Computation, 76:278-346, 1988. DOI: [10.1016/0890-5401(88)90011-9](https://doi.org/10.1016/0890-5401(88)90011-9)

<a id="ref-9"></a>[9] O. Laumann. *Elk: The Extension Language Kit Scheme Reference*, 1995. DOI未確認。

<a id="ref-10"></a>[10] T. Lindholm and F. Yellin. *The Java Virtual Machine Specification*. Second Edition. Addison-Wesley, 1999. DOI: [10.5555/553607](https://doi.org/10.5555/553607)

<a id="ref-11"></a>[11] S. Nishizaki. *ML with first-class environments and its type inference algorithm*. In *Logic, Language and Computation*, Lecture Notes in Computer Science, vol. 792, pages 95-116. Springer, 1994. DOI: [10.1007/BFb0032396](https://doi.org/10.1007/BFb0032396)

<a id="ref-12"></a>[12] S. Nishizaki. *Simply typed lambda calculus with first-class environments*. Publications of Research Institute for Mathematical Sciences, Kyoto University, 30(6):1055-1121, 1995. DOI: [10.2977/PRIMS/1195164948](https://doi.org/10.2977/PRIMS/1195164948)

<a id="ref-13"></a>[13] S. Nishizaki. *Polymorphic environment calculus and its type inference algorithm*. Higher-Order and Symbolic Computation, 13(3):239-278, 2000. DOI: [10.1023/A:1010010314528](https://doi.org/10.1023/A:1010010314528)

<a id="ref-14"></a>[14] S. Nishizaki and Y. Akama. *Translations of first-class environments to records*. In *1st International Workshop on Explicit Substitutions*, 1998. DOI未確認。

<a id="ref-15"></a>[15] M. Odersky. *A functional theory of local names*. In *Conference Record of the Twenty-First Annual ACM Symposium on Principles of Programming Languages*, pages 48-59, 1994. DOI: [10.1145/174675.175187](https://doi.org/10.1145/174675.175187)

<a id="ref-16"></a>[16] C. Queinnec and D. D. Roure. *Sharing code through first-class environments*. In *Proceedings of the 1996 ACM SIGPLAN International Conference on Functional Programming*, pages 251-261, 1996. DOI: [10.1145/232627.232653](https://doi.org/10.1145/232627.232653)

<a id="ref-17"></a>[17] M. Sato, T. Sakurai, and R. Burstall. *Explicit environments*. In *Typed Lambda Calculi and Applications*, 1999. DOI: [10.1007/3-540-48959-2_24](https://doi.org/10.1007/3-540-48959-2_24)
