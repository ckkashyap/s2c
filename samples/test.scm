

(define f (lambda (x) x))

(f (+ (call/cc
    (lambda (cont)
        (* 2 (cont  8))))
    1))
