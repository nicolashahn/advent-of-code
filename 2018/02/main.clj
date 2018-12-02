; Part 1

; Count the number of times char `c` appears in string `word`
; c: char
; word: string
; returns: int
(defn ct-char [c word]
  (count (filter #(= c %1) word)))

; Return whether any character in the string `box` appears exactly `n` times
; n: int
; box: string
; returns: bool
(defn has-n [n box]
  (def uq-chars (set box))
  (some #(= n (ct-char %1 box)) 
        uq-chars))

(assert (= 3 (ct-char \a "asdfaa")))
(assert (= 0 (ct-char \x "asdfaa")))
(assert (has-n 3 "asdfasdfa"))
(assert (has-n 2 "asdfasdfa"))
(assert (not (has-n 1 "asdfasdfa")))

(def lines (with-open [rdr (clojure.java.io/reader "in.txt")]
            (doall (map str (map read-string (line-seq rdr))))))

(def twos (count (filter true? (map (partial has-n 2) lines))))
(def threes (count (filter true? (map (partial has-n 3) lines))))

(println (* twos threes))


; Part 2
(require '[clojure.string :as str])

; TODO make this more efficient
(def pairs
  (apply concat
    (map
      (fn [x] 
        (map (fn [y] [x y]) lines))
      lines)))

(doseq [pair pairs]
  (def ch-pairs 
    (map vector (first pair) (second pair)))
  (def common 
    (filter #(= (first %) (second %)) ch-pairs))
  (if (= (count common) (dec (count ch-pairs)))
    (println (str/join (map first common)))))
