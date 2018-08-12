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
  (lambda (h w f)
    (do-times h
              (lambda (r)
                (do-times w
                          (lambda (c) (f c r)))))))


(foreach-pixel width height (lambda (r c) (pset r c 0 0 255)))

(define draw-square
  (lambda (y x s r g b)
    (do-times s (lambda (n) (pset (+ x n) y r g b)))
    (do-times s (lambda (n) (pset x (+ y n) r g b)))
    (do-times s (lambda (n) (pset (+ x s) (+ y n) r g b)))
    (do-times s (lambda (n) (pset (+ x n) (+ y s) r g b)))
    (pset (+ x s) (+ y s) r g b)
    ))

(foreach-pixel 10 10
               (lambda (r c)
                 (draw-square (+ 10 (* r 50)) (+ 0 (* c 50)) 5 255 255 0)
                 (draw-square (+ 10 (* r 50)) (+ 10 (* c 50)) 5 0 255 0)
                 (draw-square (* r 50) (+ 10 (* c 50)) 5 255 0 0)
                 (draw-square (* r 50) (* c 50) 5 255 255 255)))


1
