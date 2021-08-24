import React from 'react';

export interface FileRepresentation {
    file: File;
    dataUrl: string;
}

interface FileViewerProps {
    r: FileRepresentation
}

const FileViewer = (props: FileViewerProps) => {
    return (
        <div>
            <span>{props.r.file.name}</span>
            {props.r.dataUrl && 
                <iframe title="pdf" width="100%" height="75%" allowFullScreen src={props.r.dataUrl} />
            }
        </div>
    );
};

export default FileViewer;