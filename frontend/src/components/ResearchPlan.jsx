import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ResearchPlan = ({ plan, onStartResearch, onEditPlan }) => {
    const [expandedItems, setExpandedItems] = useState([]);
    const [isExecuting, setIsExecuting] = useState(false);

    const toggleItem = (index) => {
        setExpandedItems(prev =>
            prev.includes(index)
                ? prev.filter(i => i !== index)
                : [...prev, index]
        );
    };

    const handleStartResearch = async () => {
        setIsExecuting(true);
        await onStartResearch();
        setIsExecuting(false);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl p-6 border border-slate-700 shadow-xl mb-8"
        >
            {/* Header */}
            <div className="flex items-start gap-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                    </svg>
                </div>
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-slate-200 mb-1">
                        Here's a research plan for that topic. If you need to update it, let me know!
                    </h3>
                </div>
            </div>

            {/* Plan Title */}
            <div className="mb-4">
                <h4 className="text-xl font-bold text-white mb-3">{plan.plan_title}</h4>
            </div>

            {/* Research Steps */}
            <div className="space-y-2 mb-6">
                {/* Research Websites Section */}
                <div className="bg-slate-800/50 rounded-lg border border-slate-700">
                    <button
                        onClick={() => toggleItem(0)}
                        className="w-full px-4 py-3 flex items-center gap-3 text-left hover:bg-slate-800/70 transition-colors rounded-lg"
                    >
                        <div className="w-8 h-8 bg-slate-700 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg className="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                            </svg>
                        </div>
                        <span className="flex-1 font-medium text-slate-200">Research Websites</span>
                        <svg
                            className={`w-5 h-5 text-slate-400 transition-transform ${expandedItems.includes(0) ? 'rotate-180' : ''}`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>

                    <AnimatePresence>
                        {expandedItems.includes(0) && (
                            <motion.div
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                transition={{ duration: 0.2 }}
                                className="overflow-hidden"
                            >
                                <div className="px-4 pb-4 pt-2 space-y-2">
                                    {plan.sub_questions.map((question, idx) => (
                                        <div key={idx} className="flex gap-2 text-sm text-slate-300">
                                            <span className="text-teal-400 font-medium">({idx + 1})</span>
                                            <span>{question}</span>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                {/* Analyze Results */}
                <div className="bg-slate-800/50 rounded-lg border border-slate-700 px-4 py-3 flex items-center gap-3">
                    <div className="w-8 h-8 bg-slate-700 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    </div>
                    <span className="font-medium text-slate-200">Analyze Results</span>
                </div>

                {/* Create Report */}
                <div className="bg-slate-800/50 rounded-lg border border-slate-700 px-4 py-3 flex items-center gap-3">
                    <div className="w-8 h-8 bg-slate-700 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                    </div>
                    <span className="font-medium text-slate-200">Create Report</span>
                </div>

                {/* Ready in a few mins */}
                <div className="bg-slate-800/50 rounded-lg border border-slate-700 px-4 py-3 flex items-center gap-3">
                    <div className="w-8 h-8 bg-slate-700 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <span className="font-medium text-slate-200">Ready in a few mins</span>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 justify-end">
                <button
                    onClick={onEditPlan}
                    className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium rounded-lg transition-all duration-200 border border-slate-700 hover:border-slate-600"
                >
                    Edit plan
                </button>
                <button
                    onClick={handleStartResearch}
                    disabled={isExecuting}
                    className="px-5 py-2.5 bg-gradient-to-r from-teal-600 to-teal-500 hover:from-teal-700 hover:to-teal-600 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                    {isExecuting ? (
                        <>
                            <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                            <span>Researching...</span>
                        </>
                    ) : (
                        'Start research'
                    )}
                </button>
            </div>
        </motion.div>
    );
};

export default ResearchPlan;
