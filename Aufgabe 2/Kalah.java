package kalah;

import java.util.List;

/**
 * Hauptprogramm für KalahMuster.
 *
 * @since 29.3.2021
 * @author oliverbittel
 */
public class Kalah {

    private static final String ANSI_BLUE = "\u001B[34m";

    /**
     *
     * @param args wird nicht verwendet.
     */
    public static void main(String[] args) {
        // testExample();
        //testHHGame();
        testMiniMaxAndAlphaBetaWithGivenBoard();
        //testHumanMiniMax();
        //testHumanMiniMaxAndAlphaBeta();
    }

    /**
     * Beispiel von https://de.wikipedia.org/wiki/Kalaha
     */
    public static void testExample() {
        KalahBoard kalahBd = new KalahBoard(new int[]{5, 3, 2, 1, 2, 0, 0, 4, 3, 0, 1, 2, 2, 0}, 'B');
        
        kalahBd.print();

        System.out.println("B spielt Mulde 11");
        kalahBd.move(11);
        kalahBd.print();

        System.out.println("B darf nochmals ziehen und spielt Mulde 7");
        kalahBd.move(7);
        kalahBd.print();
    }

    /**
     * Mensch gegen Mensch
     */
    public static void testHHGame() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        while (!kalahBd.isFinished()) {
            int action = kalahBd.readAction();
            kalahBd.move(action);
            kalahBd.print();
        }

        System.out.println("\n" + ANSI_BLUE + "GAME OVER");
    }

    public static void testMiniMaxAndAlphaBetaWithGivenBoard() {
        KalahBoard kalahBd = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        // KalahBoard kalahBd = new KalahBoard(new int[]{3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0}, 'A'); // 20 - 16 Verloren
        // A ist am Zug und kann aufgrund von Bonuszügen 8-aml hintereinander ziehen!
        // A muss deutlich gewinnen!
        kalahBd.print();

        while (!kalahBd.isFinished()) {
            int action;
            if (kalahBd.getCurPlayer() == 'A') {
                // Berechnen Sie für A eine Aktion mit Ihrem Verfahren und geben Sie die Aktion auf der Konsole aus. 14 -> 26
                int Depth = 8; 
                action = MaxAction(kalahBd, Depth, Integer.MIN_VALUE, Integer.MAX_VALUE);
                System.out.println("A zieht Mulde " + action);
            }
            action = kalahBd.readAction();
            kalahBd.move(action);
            kalahBd.print();
        }

        System.out.println("\n" + ANSI_BLUE + "GAME OVER");
    }


    public static int MaxAction(KalahBoard board, int depth, int alpha, int beta) {
        int bestScore = Integer.MIN_VALUE;
        int bestMove  = -1;
        for (KalahBoard child : sortedActions(board)) {
            // depth nicht runterzählen, weil wir hier nichts wissen von Spielerwechsel
            int score = (child.getCurPlayer() == board.getCurPlayer())
                 ? MaxValue(child, depth, alpha, beta, board.getCurPlayer())
                 : MinValue(child, depth - 1, alpha, beta, board.getCurPlayer());
            if (score > bestScore) {
                bestScore = score;
                bestMove  = child.getLastPlay();
            }
            alpha = Math.max(alpha, bestScore);
        }
        return bestMove;
    }
    
    
    


    public static int MaxValue(KalahBoard board, int depth, int alpha, int beta, char previousPlayer) {
        if (depth == 0 || board.isFinished())
            return evaluate(board);
    
        int maxValue = Integer.MIN_VALUE;
        for (KalahBoard child : sortedActions(board)) {
            // nur dann depth– wenn Spieler wechselt
            int nextDepth = (child.getCurPlayer() != previousPlayer) ? depth - 1 : depth;
    
            int score;
            if (child.getCurPlayer() == previousPlayer) {
                // Bonuszug: gleicher Spieler, also wieder MaxValue
                score = MaxValue(child, nextDepth, alpha, beta, previousPlayer);
            } else {
                // normaler Zug: wechsle Rolle zu Min
                score = MinValue(child, nextDepth, alpha, beta, previousPlayer);
            }
    
            maxValue = Math.max(maxValue, score);
            alpha    = Math.max(alpha, maxValue);
            if (beta <= alpha) break;  // Beta‑Cutoff
        }
        return maxValue;
    }
    
    
    
   
    public static int MinValue(KalahBoard board, int depth, int alpha, int beta, char previousPlayer) {
        if (depth == 0 || board.isFinished())
            return evaluate(board);
    
        int minValue = Integer.MAX_VALUE;
        for (KalahBoard child : sortedActions(board)) {
            int nextDepth = (child.getCurPlayer() != previousPlayer) ? depth - 1 : depth;
    
            int score;
            if (child.getCurPlayer() == previousPlayer) {
                // Bonuszug vom Min‑Spieler – bleibt MinValue
                score = MinValue(child, nextDepth, alpha, beta, previousPlayer);
            } else {
                // normaler Zug: wechsle Rolle zu Max
                score = MaxValue(child, nextDepth, alpha, beta, previousPlayer);
            }
    
            minValue = Math.min(minValue, score);
            beta     = Math.min(beta, minValue);
            if (beta <= alpha) break;  // Alpha‑Cutoff
        }
        return minValue;
    }
    
    
     
    public static int evaluate(KalahBoard b) {
        int score = b.getAKalah() - b.getBKalah();
        if (b.isBonus()) score += 10;
        return score;
    } 


    public static List<KalahBoard> sortedActions(KalahBoard board) {
    List<KalahBoard> actions = board.possibleActions();

    actions.sort((a, b) -> {
        int scoreA = (a.isBonus() ? 10 : 0) + a.getAKalah();
        int scoreB = (b.isBonus() ? 10 : 0) + b.getAKalah();     
        return Integer.compare(scoreB, scoreA); // absteigend sortieren
    });

    return actions;
    }

    
}
