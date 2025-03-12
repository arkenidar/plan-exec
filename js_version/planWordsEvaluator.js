// planWordsEvaluator.js
// Import the logger
import { logger } from './planExecutor.js';

// Debugging related
let planEvalDebugFlag = false;

// Python-like functions
const len = (obj) => obj.length;

function debugPrint(...args) {
    if (!planEvalDebugFlag) {
        return;
    }
    // Debug print using the centralized logger
    logger.debug(...args);
}

// Code-blocks handling
function skipBlock(planWords, startI) {
    let nestedLevel = 0;
    let currentI = startI;
    
    while (currentI < planWords.length) {
        const word = planWords[currentI];
        if (word === "{") {
            nestedLevel += 1;
        } else if (word === "}") {
            nestedLevel -= 1;
            if (nestedLevel === 0) {
                const nextI = currentI + 1;
                return nextI;
            }
        }
        currentI += 1;
    }
}

function evaluateBlock(planWords, startI) {
    let evaluatedWord = null;
    let currentI = startI + 1;
    
    while (currentI < planWords.length) {
        const word = planWords[currentI];
        if (word === "}") {
            const nextI = currentI + 1;
            return [evaluatedWord, nextI];
        }
        [evaluatedWord, currentI] = evaluateWord(planWords, currentI);
    }
}

let textBuffer = "";

function evaluateWord(planWords, currentI) {
    let evaluatedWord = null;
    let nextI = null;
    const word = planWords[currentI];
    
    debugPrint("word:", word);
    nextI = currentI + 1;
    
    if (word === "pass") {
        nextI = currentI + 1;
        evaluatedWord = null;
    } else if (word === "eval") {
        [evaluatedWord, nextI] = evaluateWord(planWords, currentI + 1);
        evaluatedWord = eval(evaluatedWord);
    } else if (word === "write" || word === "writeln") {
        [evaluatedWord, nextI] = evaluateWord(planWords, currentI + 1);
        const endLine = { "write": "", "writeln": "\n" }[word];
        
        if (word === "write") {
            textBuffer += String(evaluatedWord);
        } else {
            textBuffer += String(evaluatedWord);
            console.log(textBuffer);
            textBuffer = "";
        }
    } else if (word === "log") {
        // Add a new log command that uses our logger
        [evaluatedWord, nextI] = evaluateWord(planWords, currentI + 1);
        logger.info(String(evaluatedWord));
    } else if (word === "if" || word === "if-else") {
        let condition;
        [condition, nextI] = evaluateWord(planWords, nextI);
        debugPrint("condition:", condition);
        
        if (condition === true) {
            [evaluatedWord, nextI] = evaluateBlock(planWords, nextI);
            if (word === "if-else") {
                nextI = skipBlock(planWords, nextI);
            }
        } else if (condition === false) {
            nextI = skipBlock(planWords, nextI);
            if (word === "if-else") {
                [evaluatedWord, nextI] = evaluateBlock(planWords, nextI);
            }
        } else {
            logger.error("ERROR: condition must be a boolean value");
            debugPrint("Exiting...");
            evaluatedWord = "ERROR: condition must be a boolean value";
            nextI = null;
        }
    } else if (word === "times") {
        // Evaluate the times count
        let nextIBlockStart;
        [evaluatedWord, nextIBlockStart] = evaluateWord(planWords, nextI);
        const timesCount = evaluatedWord;
        
        if (typeof timesCount !== 'number' || !Number.isInteger(timesCount)) {
            logger.error("ERROR: times_count value must be an integer");
            throw new Error("ERROR: times_count value must be an integer");
        }
        
        // Check the block start
        if (planWords[nextIBlockStart] !== "{") {
            logger.error("Block start expected");
            throw new Error("Block start expected");
        }
        
        for (let timesI = 0; timesI < timesCount; timesI++) {
            debugPrint("times_i:", timesI);
            // Evaluate the block
            [evaluatedWord, nextI] = evaluateBlock(planWords, nextIBlockStart);
            debugPrint("evaluatedWord:", evaluatedWord);
        }
        
        if (timesCount <= 0) {
            // Skip the block
            nextI = skipBlock(planWords, nextIBlockStart);
        }
    } else if (word === "len") {
        // Handle len function explicitly
        [evaluatedWord, nextI] = evaluateWord(planWords, currentI + 1);
        evaluatedWord = len(evaluatedWord);
    } else {
        try {
            // Try to evaluate the word
            if (word.startsWith('"') && word.endsWith('"')) {
                // It's a string literal
                evaluatedWord = word.slice(1, -1);
            } else if (!isNaN(Number(word))) {
                // It's a number
                evaluatedWord = Number(word);
            } else {
                // Try to evaluate as JavaScript
                evaluatedWord = eval(word);
            }
            
            debugPrint("evaluatedWord:", evaluatedWord);
            
            if (typeof evaluatedWord === 'function') {
                const callableWord = evaluatedWord;
                [evaluatedWord, nextI] = evaluateWord(planWords, currentI + 1);
                evaluatedWord = callableWord(evaluatedWord);
                debugPrint("evaluatedWord:", evaluatedWord);
            }
        } catch (error) {
            logger.error("ERROR: Unknown word:", word);
            debugPrint("Exiting...");
            evaluatedWord = "Unknown word: " + word;
            nextI = null; // exit
        }
    }
    
    // Return the evaluated word and the next index
    return [evaluatedWord, nextI];
}

function evaluatePlan(planWords, enableDebug = false) {
    // Enable debug if requested
    planEvalDebugFlag = enableDebug;
    if (enableDebug) {
        logger.debug("Starting evaluation with debug mode enabled");
    }
    
    let currentI = 0;
    while (currentI !== null && currentI < planWords.length) {
        let evaluatedWord;
        [evaluatedWord, currentI] = evaluateWord(planWords, currentI);
    }
}

// Export as ES6 module
export { evaluatePlan };