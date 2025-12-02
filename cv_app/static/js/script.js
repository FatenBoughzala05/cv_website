console.log('script.js loaded');

function printCV() {
    // Log print click first
    fetch('/log-print-click/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `lang=${encodeURIComponent(document.documentElement.lang || '')}`
    }).finally(() => {
        window.print();
    });
}

function downloadCV() {
    console.log('downloadCV function called');
    // Log download click first
    fetch('/log-download-click/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `lang=${encodeURIComponent(document.documentElement.lang || '')}`
    }).finally(() => {
        // Just request the Django endpoint → browser will download PDF
        window.location.href = "/download-cv/";
    });
}

// Attach event listeners programmatically
document.addEventListener('DOMContentLoaded', () => {
    const printButton = document.querySelector('#action-buttons button:nth-child(1)');
    const downloadButton = document.querySelector('#action-buttons button:nth-child(2)');

    if (printButton) {
        printButton.addEventListener('click', printCV);
    } else {
        console.error('Print button not found');
    }

    if (downloadButton) {
        downloadButton.addEventListener('click', downloadCV);
    } else {
        console.error('Download button not found');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const printButton = document.querySelector('#action-buttons button:nth-child(1)');
    const downloadButton = document.querySelector('#action-buttons button:nth-child(2)');

    if (printButton) {
        printButton.addEventListener('click', printCV);
    } else {
        console.error('Print button not found');
    }

    if (downloadButton) {
        downloadButton.addEventListener('click', downloadCV);
    } else {
        console.error('Download button not found');
    }
});
function adjustTimelineLines() {
    // Experience timeline
    const experienceLine = document.querySelector('.experience-timeline-line');
    const experienceContainer = document.querySelector('.experience-container');
    const experienceH3s = experienceContainer.querySelectorAll('.experience-content h3');

    if (experienceLine && experienceH3s.length >= 2) {
        const firstH3 = experienceH3s[0];
        const lastH3 = experienceH3s[experienceH3s.length - 1];

        // Position de l'élément par rapport à la fenêtre
        const firstH3Rect = firstH3.getBoundingClientRect();
        const lastH3Rect = lastH3.getBoundingClientRect();
        const containerRect = experienceContainer.getBoundingClientRect();

        // Calcul de la position 'top' de la ligne, ajustée au centre du premier point
        const topOffset = firstH3Rect.top - containerRect.top + (firstH3.offsetHeight / 2);

        // Calcul de la hauteur de la ligne
        const height = (lastH3Rect.top - firstH3Rect.top) + (lastH3.offsetHeight / 2);
        experienceLine.style.backgroundColor = '#e4d4c4'; 
        experienceLine.style.boxShadow = ' 0px 4px 8px rgba(0, 0, 0, 0.2)';
        experienceLine.style.width = '10px';
        experienceLine.style.borderRadius = '5px';
        experienceLine.style.position = 'relative';
       
        experienceLine.style.top = `${topOffset}px`;
        experienceLine.style.height = `${height}px`;
      
    } else if (experienceLine) {
        experienceLine.style.display = 'none';
    }

    // Academic timeline
    const academicLine = document.querySelector('.academic-timeline-line');
    const academicContainer = document.querySelector('.academic-container');
    const academicH3s = academicContainer.querySelectorAll('.academic-content h4');

    if (academicLine && academicH3s.length >= 2) {
        const firstH3 = academicH3s[0];
        const lastH3 = academicH3s[academicH3s.length - 1];

        // Position de l'élément par rapport à la fenêtre
        const firstH3Rect = firstH3.getBoundingClientRect();
        const lastH3Rect = lastH3.getBoundingClientRect();
        const containerRect = academicContainer.getBoundingClientRect();

        // Calcul de la position 'top' de la ligne, ajustée au centre du premier point
        const topOffset = firstH3Rect.top - containerRect.top + (firstH3.offsetHeight / 2);
        
        // Calcul de la hauteur de la ligne
        const height = (lastH3Rect.top - firstH3Rect.top) + (lastH3.offsetHeight / 2);
        academicLine.style.width = '10px';
        academicLine.style.borderRadius = '5px';
        academicLine.style.position = 'relative';
        academicLine.style.top = `${topOffset}px`;
        academicLine.style.height = `${height}px`;
        academicLine.innerHTML = '';
        const numLines = 12;
        const lineHeight = 20;
        for (let i = 0; i < numLines; i++) {
            const smallLine = document.createElement('div');
            smallLine.className = 'small-timeline-line';
            const topPos = (i * (height - lineHeight) / (numLines - 1));
            smallLine.style.position = 'absolute';
            smallLine.style.top = `${topPos}px`;
            smallLine.style.left = '0';
            smallLine.style.width = '10px';
            smallLine.style.height = `${lineHeight}px`;
            smallLine.style.backgroundColor = '#e4d4c4';
            smallLine.style.borderRadius = '3px';
            smallLine.style.boxShadow = '0px 4px 8px rgba(0, 0, 0, 0.2)';
            academicLine.appendChild(smallLine);
        }
    } else if (academicLine) {
        academicLine.style.display = 'none';
    }
}

window.addEventListener('resize', adjustTimelineLines);
window.addEventListener('load', adjustTimelineLines);
