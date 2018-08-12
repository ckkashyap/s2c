(define data (get-input-buffer))
(define width (peek32 data 0))
(define height (peek32 data 1))
(define buffer (peekptr data 1))

(define pset
  (lambda (x y r g b)
    (let ((offset (+ (* 4 (* y width)) (* x 4))))
      (poke8 buffer (+ offset 3) 255)
      (poke8 buffer (+ offset 2) r)
      (poke8 buffer (+ offset 1) g)
      (poke8 buffer (+ offset 0) b))))

(define do-times
  (lambda (i f)
    (if (= i 1) (f 0) (let () (f (- i 1)) (do-times (- i 1) f)))))

(define foreach-pixel
  (lambda (f)
    (do-times height
              (lambda (r)
                (do-times width
                          (lambda (c) (f c r)))))))


(foreach-pixel (lambda (r c) (pset r c 100 100 255)))

(define draw-square
  (lambda (x y s r g b)
    (do-times s (lambda (n) (pset (+ x n) y r g b)))
    (do-times s (lambda (n) (pset x (+ y n) r g b)))
    (do-times s (lambda (n) (pset (+ x s) (+ y n) r g b)))
    (do-times s (lambda (n) (pset (+ x n) (+ y s) r g b)))
    ))


(do-times 18 
          (lambda (n)
            (draw-square (* n 10) (* n 10) 25 255 255 255)))

1
