// Plan executor
import { wordsParse } from './planWordsParser.js';
import { evaluatePlan } from './planWordsEvaluator.js';

// Logger configuration
const LogLevel = {
    ERROR: 0,
    WARN: 1,
    INFO: 2,
    DEBUG: 3,
    VERBOSE: 4
};

class Logger {
    constructor(level = LogLevel.INFO) {
        this.level = level;
    }

    error(...args) {
        if (this.level >= LogLevel.ERROR) console.error('[ERROR]', ...args);
    }

    warn(...args) {
        if (this.level >= LogLevel.WARN) console.warn('[WARN]', ...args);
    }

    info(...args) {
        if (this.level >= LogLevel.INFO) console.info('[INFO]', ...args);
    }

    debug(...args) {
        if (this.level >= LogLevel.DEBUG) console.log('[DEBUG]', ...args);
    }

    verbose(...args) {
        if (this.level >= LogLevel.VERBOSE) console.log('[VERBOSE]', ...args);
    }

    setLevel(level) {
        this.level = level;
        this.info(`Log level set to ${Object.keys(LogLevel).find(key => LogLevel[key] === level)}`);
    }
}

// Create a global logger instance
const logger = new Logger();

// Enable debug mode by setting a higher log level
// Uncomment the next line to enable debug logs
// logger.setLevel(LogLevel.DEBUG);

// Execute the plan
function executePlan(planToExecute, debugMode = false) {
    logger.info('Executing plan');
    
    // Set debug mode for parser if requested
    const planWords = wordsParse(planToExecute, debugMode);
    
    logger.debug(`Plan parsed into ${planWords.length} words`);
    
    // Execute the plan
    try {
        evaluatePlan(planWords);
        logger.info('Plan execution completed successfully');
    } catch (error) {
        logger.error('Plan execution failed:', error);
        throw error;
    }
}

// Function to fetch and execute a plan from a file
async function executePlanFromFile(filePath, debugMode = false) {
    logger.info(`Loading plan from file: ${filePath}`);
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            logger.error(`Failed to load plan file: ${response.status}`);
            throw new Error(`Failed to load plan file: ${response.status}`);
        }
        const planContent = await response.text();
        logger.debug(`Plan file loaded, size: ${planContent.length} bytes`);
        executePlan(planContent, debugMode);
        return true;
    } catch (error) {
        logger.error('Error executing plan:', error);
        return false;
    }
}

// Browser entry point
function init() {
    // Check if a plan file was specified in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const planFile = urlParams.get('plan') || 'js_testing.plan';
    const debug = urlParams.get('debug') === 'true';
    
    // Set debug level from URL if specified
    const logLevel = urlParams.get('logLevel');
    if (logLevel && LogLevel[logLevel.toUpperCase()] !== undefined) {
        logger.setLevel(LogLevel[logLevel.toUpperCase()]);
    }
    
    logger.info(`Starting plan executor with plan: ${planFile}`);
    if (debug) {
        logger.info('Debug mode enabled');
    }
    
    // Execute the plan
    executePlanFromFile(planFile, debug).then(success => {
        if (!success) {
            logger.error('Failed to execute plan');
        }
    });
}

// Initialize when DOM is fully loaded
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}

// Export functions for use in other modules
export { executePlan, executePlanFromFile, logger, LogLevel };