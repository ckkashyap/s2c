(define data (get-input-buffer))
(define width (peek32 data 0))
(define height (peek32 data 1))
(define buffer (peekptr data 1))


(define setzeroall
  (lambda (n)
    (if (= n  3)
        (poke8 buffer n 0)
      (let ()
        (poke8 buffer (- n 0) 0)
        (poke8 buffer (- n 1) 0)
        (poke8 buffer (- n 2) 0)
        (poke8 buffer (- n 3) 0)
        (setzeroall (- n 4))))))

(define pset
  (lambda (x y r g b)
    (let ((offset (+ (* 4 (* y width)) (* x 4))))
      (poke8 buffer (+ offset 3) 255)
      (poke8 buffer (+ offset 2) r)
      (poke8 buffer (+ offset 1) g)
      (poke8 buffer (+ offset 0) b))))

(define do-times
  (lambda (i f)
    (if (= i 1) (f 1) (let () (f i) (do-times (- i 1) f)))))

(define draw-square
  (lambda (x y s r g b)
    (do-times s (lambda (n) (pset (+ x n) y r g b)))
    (do-times s (lambda (n) (pset x (+ y n) r g b)))
    (do-times s (lambda (n) (pset (+ x s) (+ y n) r g b)))
    (do-times s (lambda (n) (pset (+ x n) (+ y s) r g b)))
    ))

(setzeroall (- (* 4 (* width height)) 1))

(define start 10)
(define g (lambda (m)
(do-times 30
          (lambda (n)
(draw-square (+ (* n 4) (+ (* 1 m) (+ start 0))) (+ (* n 8) (+ (+ start 0) (* 1 5))) 100 255 0 0)
(draw-square (+ (* n 4) (+ (* 1 m) (+ start 10))) (+ (* n 8) (+ (+ start 10) (* 1 5))) 100 0 255 0)
(draw-square (+ (* n 4) (+ (* 1 m) (+ start 20))) (+ (* n 8) (+ (+ start 20) (* 1 5))) 100 0 0 255)))))


(do-times 7 (lambda (n)
              (g n)
              ))
1
