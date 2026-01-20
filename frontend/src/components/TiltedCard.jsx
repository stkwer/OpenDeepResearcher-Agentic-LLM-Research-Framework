import React, { useState, useRef } from 'react';
import { motion, useSpring } from 'framer-motion';

/**
 * TiltedCard Component
 * 
 * An interactive 3D card that tilts based on mouse position with smooth spring animations.
 * 
 * @param {Object} props
 * @param {React.ReactNode} props.children - Content to render inside the card
 * @param {number} props.rotateAmplitude - Maximum rotation in degrees (default: 15)
 * @param {number} props.scaleOnHover - Scale factor on hover (default: 1.05)
 * @param {string} props.width - Card width (default: 'auto')
 * @param {string} props.height - Card height (default: 'auto')
 * @param {string} props.className - Additional CSS classes
 * @param {React.ReactNode} props.overlayContent - Optional overlay content on hover
 */
const TiltedCard = ({
    children,
    rotateAmplitude = 15,
    scaleOnHover = 1.05,
    width = 'auto',
    height = 'auto',
    className = '',
    overlayContent = null,
}) => {
    const [isHovered, setIsHovered] = useState(false);
    const cardRef = useRef(null);

    // Spring animations for smooth, natural movement
    const springConfig = { stiffness: 300, damping: 20 };
    const rotateX = useSpring(0, springConfig);
    const rotateY = useSpring(0, springConfig);
    const scale = useSpring(1, springConfig);

    // Handle mouse movement for tilt effect
    const handleMouseMove = (e) => {
        if (!cardRef.current) return;

        const card = cardRef.current;
        const rect = card.getBoundingClientRect();

        // Calculate mouse position relative to card center
        // Values range from -1 (left/top) to 1 (right/bottom)
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const mouseX = e.clientX - centerX;
        const mouseY = e.clientY - centerY;

        // Normalize to -1 to 1 range
        const normalizedX = mouseX / (rect.width / 2);
        const normalizedY = mouseY / (rect.height / 2);

        // Calculate rotation angles
        // Invert Y axis for natural tilt (moving mouse up tilts card up)
        const rotateYValue = normalizedX * rotateAmplitude;
        const rotateXValue = -normalizedY * rotateAmplitude;

        // Update spring values
        rotateX.set(rotateXValue);
        rotateY.set(rotateYValue);
    };

    // Handle mouse enter
    const handleMouseEnter = () => {
        setIsHovered(true);
        scale.set(scaleOnHover);
    };

    // Handle mouse leave - reset to flat position
    const handleMouseLeave = () => {
        setIsHovered(false);
        rotateX.set(0);
        rotateY.set(0);
        scale.set(1);
    };

    return (
        <div
            ref={cardRef}
            onMouseMove={handleMouseMove}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            style={{
                perspective: '1000px',
                width,
                height,
            }}
            className={`relative ${className}`}
        >
            <motion.div
                style={{
                    rotateX,
                    rotateY,
                    scale,
                    transformStyle: 'preserve-3d',
                }}
                className="relative w-full h-full"
            >
                {/* Animated border glow effect - now tilts with the card */}
                <div className={`ambient-glow-container ${isHovered ? 'active animated' : ''}`}>
                    {/* Card Content */}
                    <div className="w-full h-full relative z-10">
                        {children}
                    </div>

                    {/* Overlay Content (appears on hover) */}
                    {overlayContent && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: isHovered ? 1 : 0 }}
                            transition={{ duration: 0.3 }}
                            className="absolute inset-0 flex items-center justify-center pointer-events-none z-20"
                            style={{ transform: 'translateZ(20px)' }}
                        >
                            {overlayContent}
                        </motion.div>
                    )}
                </div>
            </motion.div>
        </div>
    );
};

export default TiltedCard;

