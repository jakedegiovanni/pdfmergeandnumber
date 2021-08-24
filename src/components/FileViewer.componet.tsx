import React from 'react';

export class FileRepresentation {
    public file: File;
    public dataUrl: string;

    constructor(file: File, dataUrl: string) {
        this.file = file;
        this.dataUrl = dataUrl;
    }
}

interface FileViewerProps {
    r: FileRepresentation
}

const FileViwer = (props: FileViewerProps) => {
    return (
        <div>
            <span>{props.r.file.name}</span>
            {props.r.dataUrl && 
                <iframe title="pdf" width="100%" height="75%" allowFullScreen src={props.r.dataUrl} />
            }
        </div>
    );
};

export default FileViwer;