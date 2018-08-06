(define b (new-buffer 4))
(define ib (get-input-buffer))

(define v1
  (let (
        (x (poke8 b 0 65))
        (y (peek8 b 0))
        )

    (if (= y 65) 1 0)
    ))

(define v2
  (let (
        (x (poke16 b 0 512))
        (y (peek16 b 0))
        )

    (if (= y 512) 1 0)
    ))

(define v3
  (let (
        (x (poke32 b 0 700000))
        (y (peek32 b 0))
        )

    (if (= y 700000) 1 0)
    ))

(define v4
  (let (
        (x (peek8 ib 0))
        (y (peek8 ib 1))
        )
    (if (and (= x 65) (= y 66)) 1 0)))


(define result (+ v1 (+ v2 (+ v3 v4))))

(if (= result 4) 100 0)
