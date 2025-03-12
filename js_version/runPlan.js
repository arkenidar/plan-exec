// Node.js script to run plan files from command line
import { readFileSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { executePlan, logger, LogLevel } from './planExecutor.js';

// Set up Node.js environment
const __dirname = dirname(fileURLToPath(import.meta.url));

// Parse command line args
const args = process.argv.slice(2);
const planFile = args[0] || 'user_sample.plan';
const debug = args.includes('--debug');

// Set debug level if needed
if (debug) {
    logger.setLevel(LogLevel.DEBUG);
}

try {
    console.log(`Executing plan from file: ${planFile}`);
    const planContent = readFileSync(planFile, 'utf8');
    executePlan(planContent, debug);
    console.log('Plan execution completed');
} catch (error) {
    console.error('Error executing plan:', error.message);
    process.exit(1);
}