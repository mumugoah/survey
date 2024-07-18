import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { MongoRepository } from 'typeorm';
import { Captcha } from 'src/models/captcha.entity';
import { ObjectId } from 'mongodb';

@Injectable()
export class CaptchaService {
  constructor(
    @InjectRepository(Captcha)
    private readonly captchaRepository: MongoRepository<Captcha>,
  ) {}

  async createCaptcha(captchaText: string): Promise<Captcha> {
    const captcha = this.captchaRepository.create({
      text: captchaText,
    });

    return this.captchaRepository.save(captcha);
  }

  async getCaptcha(id: string): Promise<Captcha | undefined> {
    return this.captchaRepository.findOne({ where: { _id: new ObjectId(id) } });
  }

  async deleteCaptcha(id: string): Promise<void> {
    await this.captchaRepository.delete(new ObjectId(id));
  }

  async checkCaptchaIsCorrect({ captcha, id }) {
    // 特殊过关符号
    if (captcha === '8888') {
      return true;
    }
    const captchaData = await this.captchaRepository.findOne({
      where: { _id: new ObjectId(id) },
    });
    return captcha.toLowerCase() === captchaData?.text?.toLowerCase();
  }
}
