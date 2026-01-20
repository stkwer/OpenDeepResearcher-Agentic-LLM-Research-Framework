import React from 'react';

const ShinyText = ({
    text,
    disabled = false,
    speed = 2,
    className = ''
}) => {
    if (disabled) {
        return <span className={className}>{text}</span>;
    }

    const shinyStyle = {
        display: 'inline-block',
        background: 'linear-gradient(90deg, #2dd4bf 0%, #a78bfa 25%, #f472b6 50%, #a78bfa 75%, #2dd4bf 100%)',
        backgroundSize: '200% auto',
        WebkitBackgroundClip: 'text',
        backgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        animation: `shiny ${speed}s linear infinite`,
    };

    return (
        <>
            <style>
                {`
                    @keyframes shiny {
                        0% { background-position: 0% center; }
                        100% { background-position: 200% center; }
                    }
                `}
            </style>
            <span style={shinyStyle} className={className}>
                {text}
            </span>
        </>
    );
};

export default ShinyText;
