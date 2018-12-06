(def polymer (with-open [rdr (clojure.java.io/reader "in.txt")]
              (first (line-seq rdr))))

(def alphabet "abcdefghijklmnopqrstuvwxyz")
(def lus (map str (seq alphabet) (seq (clojure.string/upper-case alphabet))))
(def uls (map str (seq (clojure.string/upper-case alphabet)) (seq alphabet)))
(def all-pairs (vec (concat lus uls)))

; remove all instances of the pair in the polymer
(defn react-pair [poly pair]
  (clojure.string/replace poly pair ""))

; remove all instances of all pairs from the polymer
(defn react-pairs [poly pairs]
  (reduce #(react-pair %1 %2) poly pairs))

; do react-pairs continually until there are no more pairs to remove
(defn react-completely [poly pairs]
  (def poly-atom (atom poly))
  (while (< (count (react-pairs @poly-atom pairs)) (count @poly-atom))
    (swap! poly-atom react-pairs pairs))
  @poly-atom)

; Part 1
(println (count (react-completely polymer all-pairs)))


; Part 2
(println
  (apply min 
     (map #(count (react-completely
                    (clojure.string/replace
                      (clojure.string/replace 
                        polymer (str (second %1)) "")
                      (str (first %1)) "")
                    all-pairs))
          uls)))
