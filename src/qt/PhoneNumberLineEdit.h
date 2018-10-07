//PhoneNumberLineEdit.h by Telechain developers
#include <QLineEdit>

struct PhoneNumberLineEdit: public QLineEdit {
	PhoneNumberLineEdit();
	QString toPhoneNumber()const;
};
