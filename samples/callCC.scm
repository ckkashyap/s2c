

(define f (lambda (x) x))

(define result
(f (+ (call/cc
    (lambda (cont)
        (* 2 (cont  8))))
    1))
)

(if (= result 9) 100 0)
