// Extract the words of a plan
function extractWordsFromPlan(plan, debug = false) {
    // Split the plan into words
    let planWords = [];
    
    // Split the plan into lines
    const lines = plan.split("\n");
    
    if (debug) console.log(`Parsing plan with ${lines.length} lines`);
    
    for (let line of lines) {
        // Remove leading and trailing whitespaces
        line = line.trim();
        
        // Skip empty lines
        if (line === "") {
            continue;
        }
        
        // Split the line into words
        let words = line.split(" ");
        
        // Remove empty words
        words = words.filter(word => word !== "");
        
        // Check for comments
        const commentIndex = words.indexOf("#");
        if (commentIndex !== -1) {
            // Remove the words after the comment
            words = words.slice(0, commentIndex);
            if (debug) console.log(`Found comment in line: ${line}`);
        }
        
        // Add the words to the plan
        planWords.push(...words);
        
        if (debug) console.log(`Parsed line: "${line}" → [${words.join(", ")}]`);
    }
    
    // Return the words of the plan
    if (debug) console.log(`Total words extracted: ${planWords.length}`);
    return planWords;
}

// Join the words of a string into a string
function joinStringWords(planWords, debug = false) {
    // Joined words
    const joinedPlanWords = [];
    
    // String flag
    let inString = false;
    
    // String accumulator
    let string = "";
    
    if (debug) console.log(`Joining string words from ${planWords.length} words`);
    
    // Join the words of a string into a string
    for (const word of planWords) {
        // Check for strings
        // Start of a string
        if (word[0] === '"' && inString === false) {
            // Start of a string
            inString = true;
            string = word;
            
            // Check for a single word string
            if (word[word.length - 1] === '"' && word.length >= 2) {
                // End of a string
                inString = false;
                joinedPlanWords.push(string);
                if (debug) console.log(`Single word string: ${string}`);
            }
        }
        // End of a string
        else if (word[word.length - 1] === '"' && inString === true) {
            // End of a string
            inString = false;
            
            // Add the string to the joined words
            string += " " + word;
            joinedPlanWords.push(string);
            if (debug) console.log(`Complete string: ${string}`);
        }
        // Middle of a string
        else if (inString === true) {
            // Middle of a string
            // Add the word to the string
            string += " " + word;
        }
        // Normal word
        else {
            // Normal word
            joinedPlanWords.push(word);
            if (debug) console.log(`Normal word: ${word}`);
        }
    }
    
    // Return the joined words
    if (debug) console.log(`Total joined words: ${joinedPlanWords.length}`);
    return joinedPlanWords;
}

function wordsParse(planString, debug = false) {
    if (debug) console.log("Starting plan parsing");
    const planWords = extractWordsFromPlan(planString, debug);
    const result = joinStringWords(planWords, debug);
    if (debug) console.log("Plan parsing complete");
    return result;
}

// Export as ES6 module
export { wordsParse };