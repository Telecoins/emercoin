﻿//DpoCreateRecordWidget.h by Telechain developers
#pragma once
#include "NameValueLineEdits.h"
#include <QScrollArea>
class QLineEdit;
class QPlainTextEdit;
class QFormLayout;
class QLabel;

class DpoCreateRecordWidget: public QScrollArea {
	public:
		DpoCreateRecordWidget();
		NameValueLineEdits* _NVPair = 0;
		void updateSettings(bool save);
    protected:
		QLineEdit* _editName = 0;
		QLineEdit* _editSN = 0;
		QPlainTextEdit* _askSignature = 0;
		QLineEdit* _signature = 0;
		QList<QLineEdit*> _edits;
		void recalcValue();
		QLineEdit* addLineEdit(QFormLayout*form, const QString& name, const QString& text, const QString& tooltip, bool readOnly = false);
		QLabel* newLabel(const QString & s);
};
