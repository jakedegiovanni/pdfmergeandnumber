import React, { ChangeEvent, MouseEvent, useState } from 'react';
import { FileRepresentation } from './FileViewer.componet';

// const PDFDocument = require('pdfkit');
// const blobStream = require('blob-stream');

const isDefined = (x: any) => x !== null && x !== undefined;

type FileMapping = {[name: string]: FileRepresentation};

const FilePicker = () => {

    // const doc = new PDFDocument();
    // const stream = doc.pipe(blobStream());
    // doc.end();
    // stream.on('finish', () => {
    //     const blob = stream.toBlob('aplication/pdf');
    //     console.log(blob);
    //     console.log(stream.toBlobURL('application/pdf'));
    // });

    const [files, setFiles] = useState<FileMapping>({});

    const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
        const files1 = e.target.files;
        if (!isDefined(files1)) return;
        const newFiles = {...files};

        for (let i = 0; i < files1!.length; i++) {
            const fr = new FileReader();
            fr.readAsDataURL(files1![i]);
            fr.onload = e => {
                const dataUrl: string = e.target!.result as string;
                const file = files1![i];
                const name: string = files1![i].name;
                newFiles[name] = {file, dataUrl};
                // todo: get redux pulled in
            }
        }
        setFiles(newFiles);
    };

    const uploadFiles = (e: MouseEvent<HTMLButtonElement>) => {};

    return (
        <div>
            {/*{files.forEach(v => <FileViwer key={v.file.name} r={v} />)}*/}

            <input type="file" name="files" multiple onChange={changeHandler} />
            <button onClick={uploadFiles}>Upload</button>
        </div>
    );
};

export default FilePicker;